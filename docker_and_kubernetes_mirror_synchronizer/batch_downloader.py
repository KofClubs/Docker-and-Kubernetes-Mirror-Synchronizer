import logging
import os
import sys
from urllib.request import urlretrieve


def __init__():
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)


def download_by_filename_list(urlPrefix, localDir, filenameListPath):
    if not os.path.exists(filenameListPath):
        logging.error(f"{filenameListPath} not found!")
        return

    if not os.path.exists(localDir):
        os.makedirs(localDir)
        logging.info(f"New directory created: {localDir}")

    filenameList = open(filenameListPath, "r")
    filenames = filenameList.readlines()
    for filename in filenames:
        # 舍弃末元素“\n”
        urlretrieve(urlPrefix+filename[:-1], filename=localDir+filename[:-1])
        logging.info(f"File retrieved: {localDir+filename[:-1]}")
