import csv
import logging
import os
import time
import numpy as np


from skippy.data.utils import get_file_name_urn

_LOCAL_SKIPPY_STORAGE = "/openfaas-local-storage/"


def has_local_storage_file(urn: str) -> bool:
    return os.path.exists(local_storage_file(urn))


def local_storage_file(urn: str) -> str:
    file_name = get_file_name_urn(urn)
    return _LOCAL_SKIPPY_STORAGE + file_name


def load_file(path: str):
    # TODO find better solution
    content = ''
    try:
        content = np.load(path, allow_pickle=True)
    except Exception as e:
        f = open(path, 'r')
        while True:
            blk = f.read(100 * 1000 * 1000)
            content += blk
            if len(blk) < (100 * 1000 * 1000):
                break
    return content


def load_file_content_local_storage(urn: str):
    path = local_storage_file(urn)
    logging.info('Reading file path %s' % path)
    start_time = time.time()
    content = load_file(path)
    logging.info('File read in %s' % (time.time() - start_time))
    return content


def save_file_content_local_storage(content, urn: str):
    file_name = get_file_name_urn(urn)
    path = _LOCAL_SKIPPY_STORAGE + file_name
    logging.info('Save file in local storage %s' % path)
    start_time = time.time()
    try:
        np.save(path, content, allow_pickle=True)
        logging.info('File saved in %s' % (time.time() - start_time))
        return path
    except Exception as e:
        logging.error('Error trying to save file in local storage: %s', e)
