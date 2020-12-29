import xml.dom.minidom as minidom
import logging
import json
import os
from urllib.request import urlretrieve
import sys
import getopt
import gzip

from settings import LINUX_DISTRIBUTION, SOURCE, TESTING_VERSION_PERMISSION, VERSION_DEPTH, LOCAL_REPO_DIR

filelistsXmlGzUrl = "https://mirrors.aliyun.com/kubernetes/yum/repos/kubernetes-el7-x86_64/repodata/filelists.xml.gz"
urlPrefix = "https://mirrors.aliyun.com/kubernetes/yum/repos/kubernetes-el7-x86_64/Packages/"
fileExtension = ".rpm"

testingVersionPermission = True
versionDepth = 0


def __init__():
    linuxDistribution = LINUX_DISTRIBUTION
    source = SOURCE

    global testingVersionPermission, versionDepth
    testingVersionPermission = TESTING_VERSION_PERMISSION
    versionDepth = VERSION_DEPTH

    global filelistsXmlGzUrl, urlPrefix, fileExtension
    # TODO RedHat系发行版
    if linuxDistribution == "centos":
        fileExtension = ".rpm"
        if source == "aliyun":
            filelistsXmlGzUrl = "https://mirrors.aliyun.com/kubernetes/yum/repos/kubernetes-el7-x86_64/repodata/filelists.xml.gz"
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
    if not os.path.exists("/tmp/package_lists"):
        os.makedirs("/tmp/package_lists")
        logging.info("New directory created: /tmp/package_lists.")

    global filelistsXmlGzUrl
    urlretrieve(filelistsXmlGzUrl,
                filename="/tmp/package_lists/filelists.xml.gz")
    logging.info(
        "filelists.xml.gz downloaded: /tmp/package_lists/filelists.xml.gz.")

    gzFile = gzip.open("/tmp/package_lists/filelists.xml.gz", "rb")
    xmlFile = open("/tmp/package_lists/filelists.xml", "w")
    content = gzFile.read()
    xmlFile.write(content.decode("utf-8"))
    logging.info("filelists.xml created: /tmp/package_lists/filelists.xml.")
    gzFile.close()
    xmlFile.close()


def get_pkg_tags():
    if not os.path.exists("/tmp/package_lists/filelists.xml"):
        logging.error("filelists.xml not found!")
        return

    domTree = minidom.parse("/tmp/package_lists/filelists.xml")
    collection = domTree.documentElement

    if collection.hasAttribute("packages"):
        numOfPkgs = int(collection.getAttribute("packages"))
        logging.info(f"This source provides a total of {numOfPkgs} packages.")

    pkgs = collection.getElementsByTagName("package")

    numOfiter = 0

    pkgTagsFile = open("/tmp/package_lists/pkg_tags.list", "a")

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

        pkgTagInUrl = pkgid+"-"+pkgName+"-"+ver+"-"+verRel+"."+pkgArch

        pkgTagsFile.write(pkgTagInUrl+"\n")

    pkgTagsFile.close()


def create_local_repo():
    if not os.path.exists("/tmp/package_lists/pkg_tags.list"):
        logging.error("pkg_tags.list not found!")
        return

    global urlPrefix, fileExtension
    if not os.path.exists(LOCAL_REPO_DIR+"Packages/"):
        os.makedirs(LOCAL_REPO_DIR+"Packages/")
        logging.info(f"New directory created: {LOCAL_REPO_DIR}Packages.")

    pkgTagsFile = open("/tmp/package_lists/pkg_tags.list", "r")
    pkgTags = pkgTagsFile.readlines()
    for pkgTagInUrl in pkgTags:
        url = urlPrefix+pkgTagInUrl[:-1]+fileExtension  # 舍弃末元素“\n”
        urlretrieve(url, filename=LOCAL_REPO_DIR +
                    "Packages/"+pkgTagInUrl[:-1]+fileExtension)

    os.system(f"createrepo {LOCAL_REPO_DIR}")


def clean_tmp_files():
    if os.path.exists("/tmp/package_lists/filelists.xml.gz"):
        os.remove("/tmp/package_lists/filelists.xml.gz")
        logging.info("filelists.xml.gz deleted.")

    if os.path.exists("/tmp/package_lists/filelists.xml"):
        os.remove("/tmp/package_lists/filelists.xml")
        logging.info("filelists.xml deleted.")

    if os.path.exists("/tmp/package_lists/pkg_tags.list"):
        os.remove("/tmp/package_lists/pkg_tags.list")
        logging.info("pkg_tags.list deleted.")


if __name__ == "__main__":
    download_filelists()
    get_pkg_tags()
    create_local_repo()
