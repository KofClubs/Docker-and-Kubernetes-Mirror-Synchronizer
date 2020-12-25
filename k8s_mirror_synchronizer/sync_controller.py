import xml.dom.minidom as minidom
import logging
import json
import os
from urllib.request import urlretrieve

domTree = minidom.parse("test.xml")
collection = domTree.documentElement

# 获得软件包数目
if collection.hasAttribute("packages"):
    numOfPkgs = int(collection.getAttribute("packages"))

pkgs = collection.getElementsByTagName("package")

numOfiter = 0

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

    pkgInfo = {"pkgid": pkgid, "name": pkgName, "arch": pkgArch,
               "epoch": verEpoch, "ver": ver, "rel": verRel}
    logging.info(json.dumps(pkgInfo))

    pkgInfoInUrl = pkgid+"-"+pkgName+"-"+ver+"-"+verRel+"."+pkgArch

    url = "https://mirrors.aliyun.com/kubernetes/yum/repos/kubernetes-el7-x86_64/Packages/"+pkgInfoInUrl+".rpm"

    if not os.path.exists("Packages"):
        os.makedirs("Packages")

    urlretrieve(url, filename="Packages/"+pkgInfoInUrl+".rpm")
