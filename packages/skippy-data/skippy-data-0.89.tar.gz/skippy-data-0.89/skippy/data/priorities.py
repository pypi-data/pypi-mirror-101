import logging
import os
from typing import List

from skippy.data.redis import get_files_size, get_dl_bandwidth, get_storage_bucket, \
    get_storage_nodes
from skippy.data.utils import get_bucket_urn, is_prediction_enabled


def get_best_node(urn: str, estimated_file_size=None, upload=False):
    if not is_prediction_enabled():
        return None

    node_name = os.environ.get('node', None)
    logging.debug("Node %s" % node_name)

    file_size = get_files_size(urn)
    if estimated_file_size is None and file_size is None:
        return None
    elif file_size is None:
        file_size = estimated_file_size

    localities = ["edge", "cloud"]
    best_node = None
    for locality in localities:
        storage_nodes = get_storage_bucket(get_bucket_urn(urn),locality) if upload else get_storage_nodes(urn, locality)
        logging.info('Storage Nodes filtered at %s %s' % (locality, storage_nodes))
        best_node = calculate_best_storage_node(storage_nodes, node_name, file_size, urn)
        if best_node:
            break
    return best_node


def calculate_best_storage_node(storage_nodes: List[str], node_name, file_size, urn: str):
    time = 0
    max_bw = 0
    max_bw_storage = None
    logging.debug('Calculations node [%s] to storage options %s to transfer %s' % (node_name, storage_nodes, urn))
    for storage in storage_nodes:
        logging.debug('Node [%s] to storage [%s]' % (node_name, storage))
        if storage == node_name:
            logging.debug('Node and storage the same. Time = 0')
            return storage

        bandwidth = get_dl_bandwidth(storage, node_name)
        if bandwidth is not None and bandwidth > max_bw:
            max_bw = bandwidth
            max_bw_storage = storage

    if max_bw_storage and file_size:
        time += int(file_size / max_bw)
    logging.debug('[%s] is the best storage from node [%s] to transfer %s. Time = %s' % (
        max_bw_storage, node_name, urn, time))
    return max_bw_storage
