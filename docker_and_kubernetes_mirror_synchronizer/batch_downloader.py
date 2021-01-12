from datetime import datetime
import logging
import os
import socket
import sys
from urllib.request import urlretrieve


def __init__():
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)


'''
安全可靠地下载文件
直接调用urlretrieve来下载文件是不可靠的，可能出现下载失败残留不完整文件的情况
为了追求下载成功率，保证文件完整性，我缺省地设计了10次失败重试，如果最终失败，则删除残留文件
@param 下载源URL、本地目标文件、最大失败重试计数
@return 是否成功、成功/最终失败的时间戳
'''


def safe_retrieve(srcUrl, distFilename, maxRetryCount=10):
    retry_count = 0
    while retry_count < maxRetryCount:
        try:
            urlretrieve(srcUrl, filename=distFilename)
            logging.info(f"File retrieved, from {srcUrl} to {distFilename}")
            # 时间格式：ISO 8601，下同
            return True, datetime.now().strftime("%Y-%m-%d")+"T"+datetime.now().strftime("%H:%M:%S")+"+08:00"
        except socket.timeout:
            retry_count += 1
            if retry_count < maxRetryCount:
                logging.warn(
                    f"Retrieving file from {srcUrl} to {distFilename} failed, retrying...")
            else:
                logging.error(
                    f"Retrieving file from {srcUrl} to {distFilename} failed, canceled!")
                # 为了保证安全，不能保留不完整的文件
                if os.path.exists(distFilename):
                    os.remove(distFilename)
                return False, datetime.now().strftime("%Y-%m-%d")+"T"+datetime.now().strftime("%H:%M:%S")+"+08:00"


'''
给定下载源URL前缀（在它后面追加文件名即可下载）、本地目标目录和文件名列表路径，执行安全下载
'''


def download_by_filename_list(urlPrefix, localDir, filenameListPath):
    if not os.path.exists(filenameListPath):
        logging.error(f"{filenameListPath} not found!")
        return

    if not os.path.exists(localDir):
        os.makedirs(localDir)
        logging.info(f"New directory created: {localDir}")

    filenameList = open(filenameListPath, "r")
    filenames = filenameList.readlines()
    latestSyncTimestamp = ""  # 最近更新时间戳，留空表示未更新
    failedList = []  # 失败列表
    for filename in filenames:
        # 我觉得在这里判断文件是否存在不是优雅的实现，虽然可以工作，但是我想把这个模块做成一个纯净的下载器，暂且不折腾了
        if os.path.exists(localDir+filename[:-1]):
            logging.info(f"{localDir+filename[:-1]} existed, skipped.")
            continue
        # 舍弃末元素“\n”
        flag, timestamp = safe_retrieve(
            srcUrl=urlPrefix + filename[:-1], distFilename=localDir+filename[:-1])
        # 下载成功，更新时间戳；否则别看你今天闹得欢，小心今后拉清单
        if flag:
            latestSyncTimestamp = timestamp
        else:
            failedList.append(filename)
    filenameList.close()
    # TODO 重新下载失败列表的文件
    # 我们应该不断地尝试下载失败列表，直到成功
    return latestSyncTimestamp, failedList
