import json
import logging
import os
import sys
import xml.dom.minidom as minidom


def __init__():
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)


def get_docker_pkg_filenames(filelistsXmlPath, pkgFilenameListPath, fileExtension):
    if not os.path.exists(filelistsXmlPath):
        logging.error(f"{filelistsXmlPath} not found!")
        return

    domTree = minidom.parse(filelistsXmlPath)
    collection = domTree.documentElement

    if collection.hasAttribute("packages"):
        numOfPkgs = int(collection.getAttribute("packages"))
        logging.info(f"This source provides a total of {numOfPkgs} packages.")

    pkgs = collection.getElementsByTagName("package")

    numOfiter = 0

    pkgFilenameList = open(pkgFilenameListPath, "w")

    for pkg in pkgs:
        numOfiter += 1

        if pkg.hasAttribute("name"):
            pkgName = pkg.getAttribute("name")
        else:
            logging.error(f"name not found, pkg No.{numOfiter}")
        if pkg.hasAttribute("arch"):
            pkgArch = pkg.getAttribute("arch")
        else:
            logging.warn(f"arch not found, pkg No.{numOfiter}")

        version = pkg.getElementsByTagName("version")[0]
        if version.hasAttribute("ver"):
            ver = version.getAttribute("ver")
        else:
            logging.warn(f"ver not found, pkg No.{numOfiter}")
        if version.hasAttribute("rel"):
            verRel = version.getAttribute("rel")
        else:
            logging.warn(f"rel not found, pkg No.{numOfiter}")

        pkgTag = {"name": pkgName, "arch": pkgArch, "ver": ver, "rel": verRel}
        logging.info(json.dumps(pkgTag))

        pkgFilename = pkgName+"-"+ver+"-"+verRel+"."+pkgArch+fileExtension

        pkgFilenameList.write(pkgFilename+"\n")

    pkgFilenameList.close()


def get_kubernetes_pkg_filenames(filelistsXmlPath, pkgFilenameListPath, fileExtension):
    if not os.path.exists(filelistsXmlPath):
        logging.error(f"{filelistsXmlPath} not found!")
        return

    domTree = minidom.parse(filelistsXmlPath)
    collection = domTree.documentElement

    if collection.hasAttribute("packages"):
        numOfPkgs = int(collection.getAttribute("packages"))
        logging.info(f"This source provides a total of {numOfPkgs} packages.")

    pkgs = collection.getElementsByTagName("package")

    numOfiter = 0

    pkgFilenameList = open(pkgFilenameListPath, "w")

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
        if version.hasAttribute("ver"):
            ver = version.getAttribute("ver")
        else:
            logging.warn(f"ver not found, pkg No.{numOfiter}")
        if version.hasAttribute("rel"):
            verRel = version.getAttribute("rel")
        else:
            logging.warn(f"rel not found, pkg No.{numOfiter}")

        pkgTag = {"pkgid": pkgid, "name": pkgName,
                  "arch": pkgArch, "ver": ver, "rel": verRel}
        logging.info(json.dumps(pkgTag))

        pkgFilename = pkgid+"-"+pkgName+"-"+ver+"-"+verRel+"."+pkgArch+fileExtension

        pkgFilenameList.write(pkgFilename+"\n")

    pkgFilenameList.close()
