import logging
import pathlib
from datetime import date
from imp import reload

import pandas as pd
from io import StringIO

from dask_ml.model_selection import train_test_split

import logging
import numpy as np
from sklearn import metrics
from sklearn.ensemble import RandomForestRegressor
# from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from skippy.data.decorator import consume, produce
import dask.dataframe as dd
import numpy as np
import dask.array as da


@consume()
@produce()
def handle(req, data=None):
    print(date)
    logging.getLogger().setLevel(logging.DEBUG)
    # logging.info("data file received %d" % len(data['pre-processed/data_1_5GB.csv']))
    # logging.info("data file received %d MB" % (len(data['pre-processed/data_1_5GB.csv']) / (1024 ** 2)))
    # data_decoded = str(data['pre-processed/data_350M.csv'])
    dataset = dd.read_csv('openfaas-local-storage/data_35M.csv', sep=",")
    #dataset = dd.delayed(pd.read_csv)('openfaas-local-storage/data_1_5GB.csv', sep=",")
    dataset.head()

    x = dataset.iloc[:, 0:4].values
    #x.compute_chunk_sizes()
    y = dataset.iloc[:, 4].values
    x_np = np.asarray(x, dtype=np.float32)
    y_np = np.asarray(y, dtype=np.int32)


    pre_model = train_test_split(x_np, y_np, test_size=0.2, random_state=0)
    # X_train, X_test, y_train, y_test = train_test_split(x, y, test_size=0.2)
    logging.info("Pre-Processed finished")
    return pre_model


@consume()
@produce()
def handle2(req, data=None):
    x_train = bytes_to_numpy(data['pre-processed/pre-model.npy'], 0, 4)
    x_test = bytes_to_numpy(data['pre-processed/pre-model.npy'], 1, 4)
    y_train = bytes_to_numpy(data['pre-processed/pre-model.npy'], 2)

    sc = StandardScaler()
    x_train = sc.fit_transform(x_train)
    x_test = sc.transform(x_test)

    regressor = RandomForestRegressor(n_estimators=200, random_state=0)
    logging.info("Start training")
    regressor.fit(x_train, y_train)
    y_pred_data = regressor.predict(x_test)
    logging.info("Training finished")
    return y_pred_data

@consume()
@produce()
def handle3(req, data=None):
    logging.info("start function")
    logging.info("pre model file received %d MB" % (len(data['pre-processed/pre-model-35.npy']) / (1024 ** 2)))
    # model = np.load(data['trained-models/model-35.npy'], allow_pickle=True)
    model =  data['trained-models/model-35.npy']
    model = model.reshape((len(model) // 1, 1))
    logging.info("model loaded generated")
    y_test = bytes_to_numpy(data['pre-processed/pre-model-35.npy'], 3)
    logging.info("y test generated")

    logging.info("Start Evaluation")
    logging.info('Mean Absolute Error (MAE): %s ' % metrics.mean_absolute_error(y_test, model))
    logging.info('Mean Squared Error (MSE):%s' % metrics.mean_squared_error(y_test, model))
    logging.info('Root Mean Squared Error (RMSE): %s ' % np.sqrt(metrics.mean_squared_error(y_test, model)))
    mape = np.mean(np.abs((y_test - model) / np.abs(y_test)))
    logging.info('Mean Absolute Percentage Error (MAPE): %s' % round(mape * 100, 2))
    logging.info('Accuracy: %s ' % round(100 * (1 - mape), 2))
    logging.info("Evaluation Finished")


def main():
    handle('aaaaaaa')
    #handle2('bbbbbbbbbb')
    #handle3("a")
    # files = download_files(urns=None)
    # upload_file(json.dumps(files),urn=None)


def bytes_to_numpy(bytes, index: int = 1, shape: int = 1) -> np.array:
    arr = np.frombuffer(bytes[index])
    return arr.reshape((len(arr) // shape, shape))


if __name__ == '__main__':
    main()
    print("Fisnihed")
