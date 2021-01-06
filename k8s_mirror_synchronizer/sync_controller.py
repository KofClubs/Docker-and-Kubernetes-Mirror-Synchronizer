import xml.dom.minidom as minidom
import logging
import json
import os
from urllib.request import urlretrieve
import sys
import getopt
import gzip

from settings import LINUX_DISTRIBUTION, SOURCE, TESTING_VERSION_PERMISSION, VERSION_DEPTH, LOCAL_REPO_DIR
from batch_downloader import download_by_filename_list

# 软件包列表压缩包下载源前缀，包含在repodata目录下，追加软件包列表文件名即可下载，缺省值：阿里云Kubernetes镜像
filelistsXmlGzUrlPrefix = "https://mirrors.aliyun.com/kubernetes/yum/repos/kubernetes-el7-x86_64/repodata/"
# 软件包列表压缩包下载目标目录，缺省值：Kubernetes镜像对应的临时目录
filelistsDir = "/tmp/kubernetes/package_lists/"
# 软件包列表压缩包文件名
filelistsXmlGzFilename = "filelists.xml.gz"
# 软件包列表文件名，缺省值：Kubernetes镜像
filelistsXmlFilename = "kubernetes_filelists.xml"
# 软件包下载源前缀，追加软件包名即可下载，缺省值：阿里云Kubernetes镜像
urlPrefix = "https://mirrors.aliyun.com/kubernetes/yum/repos/kubernetes-el7-x86_64/Packages/"
# 软件包拓展名，例如deb、rpm...
fileExtension = ".rpm"

testingVersionPermission = True
versionDepth = 0


def __init__():
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)

    linuxDistribution = LINUX_DISTRIBUTION
    source = SOURCE

    global testingVersionPermission, versionDepth
    testingVersionPermission = TESTING_VERSION_PERMISSION
    versionDepth = VERSION_DEPTH

    global filelistsXmlGzUrlPrefix, filelistsDir, filelistsXmlGzFilename, filelistsXmlFilename, urlPrefix, fileExtension
    # TODO RedHat系发行版
    if linuxDistribution == "centos":
        fileExtension = ".rpm"
        if source == "aliyun":
            filelistsXmlGzUrlPrefix = "https://mirrors.aliyun.com/kubernetes/yum/repos/kubernetes-el7-x86_64/repodata/"
            filelistsDir = "/tmp/kubernetes/package_lists/"
            filelistsXmlGzFilename = "filelists.xml.gz"
            filelistsXmlFilename = "kubernetes_filelists.xml"
            urlPrefix = "https://mirrors.aliyun.com/kubernetes/yum/repos/kubernetes-el7-x86_64/Packages/"
            logging.info("Source of mirrors is set to Aliyun.")
        elif source == "google":
            # TODO
            logging.info("Source of mirrors is set to Google.")
        # TODO
        else:
            # TODO
            logging.error("Source of mirrors is unsupported/illegal!")
        logging.info("Linux distribution is set to Red Hat.")
    # TODO Debian系发行版
    elif linuxDistribution == "debian":
        fileExtension = ".deb"
        if source == "aliyun":
            # TODO
            logging.info("Source of mirrors is set to Aliyun.")
        elif source == "google":
            # TODO
            logging.info("Source of mirrors is set to Google.")
        # TODO
        else:
            # TODO
            logging.error("Source of mirrors is unsupported/illegal!")
        logging.info("Linux distribution is set to Debian.")
    # TODO 其他发行版
    else:
        logging.error("Linux distribution is unsupported/illegal!")


def download_filelists():
    global filelistsXmlGzUrlPrefix, filelistsDir, filelistsXmlGzFilename, filelistsXmlFilename
    if not os.path.exists(filelistsDir):
        os.makedirs(filelistsDir)
        logging.info(f"New directory created: {filelistsDir}.")

    urlretrieve(filelistsXmlGzUrlPrefix+filelistsXmlGzFilename,
                filename=filelistsDir+filelistsXmlGzFilename)
    logging.info(
        f"{filelistsXmlGzFilename} downloaded: {filelistsDir+filelistsXmlGzFilename}.")

    gzFile = gzip.open(filelistsDir+filelistsXmlGzFilename, "rb")
    xmlFile = open(filelistsDir+filelistsXmlFilename, "w")
    content = gzFile.read()
    xmlFile.write(content.decode("utf-8"))
    logging.info(
        f"{filelistsXmlFilename} created: {filelistsDir+filelistsXmlFilename}.")
    gzFile.close()
    xmlFile.close()


def get_kubernetes_pkg_filenames():
    global filelistsDir, filelistsXmlFilename
    if not os.path.exists(filelistsDir+filelistsXmlFilename):
        logging.error(f"{filelistsXmlFilename} not found!")
        return

    domTree = minidom.parse(filelistsDir+filelistsXmlFilename)
    collection = domTree.documentElement

    if collection.hasAttribute("packages"):
        numOfPkgs = int(collection.getAttribute("packages"))
        logging.info(f"This source provides a total of {numOfPkgs} packages.")

    pkgs = collection.getElementsByTagName("package")

    numOfiter = 0

    pkgFilenameList = open(filelistsDir+"kubernetes_filename.list", "a")

    for pkg in pkgs:

        numOfiter += 1

        if pkg.hasAttribute("pkgid"):
            pkgid = pkg.getAttribute("pkgid")
        else:
            logging.error(f"pkgid not found, pkg No.{numOfiter}")
            continue
        if pkg.hasAttribute("name"):
            pkgName = pkg.getAttribute("name")
        else:
            logging.warn(f"name not found, pkg No.{numOfiter}")
        if pkg.hasAttribute("arch"):
            pkgArch = pkg.getAttribute("arch")
        else:
            logging.warn(f"arch not found, pkg No.{numOfiter}")

        version = pkg.getElementsByTagName("version")[0]
        if version.hasAttribute("epoch"):
            verEpoch = version.getAttribute("epoch")
        else:
            logging.warn(f"epoch not found, pkg No.{numOfiter}")
        if version.hasAttribute("ver"):
            ver = version.getAttribute("ver")
        else:
            logging.warn(f"ver not found, pkg No.{numOfiter}")
        if version.hasAttribute("rel"):
            verRel = version.getAttribute("rel")
        else:
            logging.warn(f"rel not found, pkg No.{numOfiter}")

        pkgTag = {"pkgid": pkgid, "name": pkgName, "arch": pkgArch,
                  "epoch": verEpoch, "ver": ver, "rel": verRel}
        logging.info(json.dumps(pkgTag))

        pkgFilename = pkgid+"-"+pkgName+"-"+ver+"-"+verRel+"."+pkgArch+fileExtension

        pkgFilenameList.write(pkgFilename+"\n")

    pkgFilenameList.close()


def clean_tmp_files():
    global filelistsDir, filelistsXmlGzFilename, filelistsXmlFilename
    if os.path.exists(filelistsDir+filelistsXmlGzFilename):
        os.remove(filelistsDir+filelistsXmlGzFilename)
        logging.info(f"{filelistsXmlGzFilename} deleted.")

    if os.path.exists(filelistsDir+filelistsXmlFilename):
        os.remove(filelistsDir+filelistsXmlFilename)
        logging.info(f"{filelistsXmlFilename} deleted.")

    if os.path.exists(filelistsDir+"kubernetes_filename.list"):
        os.remove(filelistsDir+"kubernetes_filename.list")
        logging.info("kubernetes_filename.list deleted.")


if __name__ == "__main__":
    download_filelists()
    get_kubernetes_pkg_filenames()
    download_by_filename_list(
        urlPrefix, LOCAL_REPO_DIR+"Packages/", filelistsDir+"kubernetes_filename.list")
    os.system(f"createrepo {LOCAL_REPO_DIR}")
