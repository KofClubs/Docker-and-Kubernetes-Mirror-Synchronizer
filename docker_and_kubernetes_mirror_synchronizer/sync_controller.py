import gzip
import logging
import os
import sys
from urllib.request import urlretrieve

from settings import(
    DOCKER_OR_KUBERNETES,

    LINUX_DISTRIBUTION,
    LINUX_DISTRIBUTION_VERSION,
    LINUX_DISTRIBUTION_ARCHITECTURE,

    DOCKER_SOURCE,
    DOCKER_BRANCH,

    KUBERNETES_SOURCE,

    LOCAL_REPO_DIR
)
from filelists_xml_parser import get_docker_pkg_filenames, get_kubernetes_pkg_filenames
from batch_downloader import download_by_filename_list

# 软件包列表压缩包下载源前缀，包含在repodata目录下，追加软件包列表文件名即可下载
filelistsXmlGzUrlPrefix = ""
# 软件包列表压缩包下载目标目录
filelistsDir = ""
# 软件包列表压缩包文件名
filelistsXmlGzFilename = ""
# 软件包列表文件名
filelistsXmlFilename = ""
# 软件包下载源前缀，追加软件包名即可下载，缺省值：阿里云Kubernetes镜像
urlPrefix = ""
# 软件包拓展名，例如deb、rpm...
fileExtension = ""


def __init__():
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)

    global filelistsXmlGzUrlPrefix, filelistsDir, filelistsXmlGzFilename, filelistsXmlFilename, urlPrefix, fileExtension

    if DOCKER_OR_KUBERNETES == "docker":
        # TODO RedHat系发行版
        if LINUX_DISTRIBUTION == "centos":
            fileExtension = ".rpm"
            if DOCKER_SOURCE == "aliyun":
                filelistsXmlGzUrlPrefix = f"https://mirrors.aliyun.com/docker-ce/linux/centos/{LINUX_DISTRIBUTION_VERSION}/{LINUX_DISTRIBUTION_ARCHITECTURE}/{DOCKER_BRANCH}/repodata/"
                filelistsDir = "/tmp/docker/package_lists/"
                ##########
                # TODO 这样的实现非常糟糕，只在不确定的短期内有效，在测试通过后必须修改！
                if LINUX_DISTRIBUTION_VERSION == "7":
                    filelistsXmlGzFilename = "9fb269ce35ec3e0980ade1963547657afe2a21ac962d5d46c80eb4a28fa22dd6-filelists.xml.gz"
                else:
                    filelistsXmlGzFilename = "4f4228eb3311ea0aa989899650e160033723d95d534dfcfc2f028bd59214c99f-filelists.xml.gz"
                ##########
                filelistsXmlFilename = "docker_filelists.xml"
                urlPrefix = f"https://mirrors.aliyun.com/docker-ce/linux/centos/{LINUX_DISTRIBUTION_VERSION}/{LINUX_DISTRIBUTION_ARCHITECTURE}/{DOCKER_BRANCH}/Packages/"
                logging.info("Source of mirrors is set to Aliyun.")
            elif DOCKER_SOURCE == "google":
                # TODO
                logging.info("Source of mirrors is set to Google.")
            # TODO 其他软件源
            else:
                # TODO
                logging.error("Source of mirrors is unsupported/illegal!")
                sys.exit()
            logging.info("Linux distribution is set to Red Hat.")
        # TODO Debian系发行版
        elif LINUX_DISTRIBUTION == "debian":
            fileExtension = ".deb"
            if DOCKER_SOURCE == "aliyun":
                # TODO
                logging.info("Source of mirrors is set to Aliyun.")
            elif DOCKER_SOURCE == "google":
                # TODO
                logging.info("Source of mirrors is set to Google.")
            # TODO
            else:
                # TODO
                logging.error("Source of mirrors is unsupported/illegal!")
                sys.exit()
            logging.info("Linux distribution is set to Debian.")
        # TODO 其他发行版
        else:
            logging.error("Linux distribution is unsupported/illegal!")
            sys.exit()
    elif DOCKER_OR_KUBERNETES == "kubernetes":
        # TODO RedHat系发行版
        if LINUX_DISTRIBUTION == "centos":
            fileExtension = ".rpm"
            if KUBERNETES_SOURCE == "aliyun":
                filelistsXmlGzUrlPrefix = "https://mirrors.aliyun.com/kubernetes/yum/repos/kubernetes-el7-x86_64/repodata/"
                filelistsDir = "/tmp/kubernetes/package_lists/"
                filelistsXmlGzFilename = "filelists.xml.gz"
                filelistsXmlFilename = "kubernetes_filelists.xml"
                urlPrefix = "https://mirrors.aliyun.com/kubernetes/yum/repos/kubernetes-el7-x86_64/Packages/"
                logging.info("Source of mirrors is set to Aliyun.")
            elif KUBERNETES_SOURCE == "google":
                # TODO
                logging.info("Source of mirrors is set to Google.")
            # TODO 其他软件源
            else:
                # TODO
                logging.error("Source of mirrors is unsupported/illegal!")
                sys.exit()
            logging.info("Linux distribution is set to Red Hat.")
        # TODO Debian系发行版
        elif LINUX_DISTRIBUTION == "debian":
            fileExtension = ".deb"
            if KUBERNETES_SOURCE == "aliyun":
                # TODO
                logging.info("Source of mirrors is set to Aliyun.")
            elif KUBERNETES_SOURCE == "google":
                # TODO
                logging.info("Source of mirrors is set to Google.")
            # TODO
            else:
                # TODO
                logging.error("Source of mirrors is unsupported/illegal!")
                sys.exit()
            logging.info("Linux distribution is set to Debian.")
        # TODO 其他发行版
        else:
            logging.error("Linux distribution is unsupported/illegal!")
            sys.exit()
    else:
        logging.error(
            "Environment variable DOCKER_OR_KUBERNETES is unsupported/illegal!")
        sys.exit()


def download_filelists():
    global filelistsXmlGzUrlPrefix, filelistsDir, filelistsXmlGzFilename, filelistsXmlFilename
    if not os.path.exists(filelistsDir):
        os.makedirs(filelistsDir)
        logging.info(f"New directory created: {filelistsDir}")

    urlretrieve(filelistsXmlGzUrlPrefix+filelistsXmlGzFilename,
                filename=filelistsDir+filelistsXmlGzFilename)
    logging.info(
        f"{filelistsXmlGzFilename} downloaded: {filelistsDir+filelistsXmlGzFilename}")

    gzFile = gzip.open(filelistsDir+filelistsXmlGzFilename, "rb")
    xmlFile = open(filelistsDir+filelistsXmlFilename, "w")
    content = gzFile.read()
    xmlFile.write(content.decode("utf-8"))
    logging.info(
        f"{filelistsXmlFilename} created: {filelistsDir+filelistsXmlFilename}")
    gzFile.close()
    xmlFile.close()


def clean_tmp_files():
    global filelistsDir, filelistsXmlGzFilename, filelistsXmlFilename
    if os.path.exists(filelistsDir+filelistsXmlGzFilename):
        os.remove(filelistsDir+filelistsXmlGzFilename)
        logging.info(f"Deleted {filelistsXmlGzFilename}")

    if os.path.exists(filelistsDir+filelistsXmlFilename):
        os.remove(filelistsDir+filelistsXmlFilename)
        logging.info(f"Deleted {filelistsXmlFilename}")

    if os.path.exists(filelistsDir+f"{DOCKER_OR_KUBERNETES}_filename.list"):
        os.remove(filelistsDir+f"{DOCKER_OR_KUBERNETES}_filename.list")
        logging.info(f"Deleted {DOCKER_OR_KUBERNETES}_filename.list")


if __name__ == "__main__":
    __init__()
    download_filelists()

    localRepoDir = ""
    if DOCKER_OR_KUBERNETES == "docker":
        get_docker_pkg_filenames(filelistsDir+filelistsXmlFilename,
                                 filelistsDir+f"{DOCKER_OR_KUBERNETES}_filename.list", fileExtension)
        localRepoDir = LOCAL_REPO_DIR + \
            f"docker-ce/linux/{LINUX_DISTRIBUTION}/{LINUX_DISTRIBUTION_VERSION}/{LINUX_DISTRIBUTION_ARCHITECTURE}/{DOCKER_BRANCH}/"
    elif DOCKER_OR_KUBERNETES == "kubernetes":
        get_kubernetes_pkg_filenames(filelistsDir+filelistsXmlFilename,
                                     filelistsDir+f"{DOCKER_OR_KUBERNETES}_filename.list", fileExtension)
        if LINUX_DISTRIBUTION == "centos":
            localRepoDir = LOCAL_REPO_DIR+f"kubernetes/yum/repos/kubernetes-el7-x86_64/"
        elif LINUX_DISTRIBUTION == "debian":
            # TODO
            print("debian")
        else:
            logging.error("Linux distribution is unsupported/illegal!")
            sys.exit()
    else:
        logging.error(
            "Environment variable DOCKER_OR_KUBERNETES is unsupported/illegal!")
        sys.exit()
    download_by_filename_list(urlPrefix, localRepoDir+"Packages/",
                              filelistsDir+f"{DOCKER_OR_KUBERNETES}_filename.list")
    os.system(f"createrepo {localRepoDir}")
