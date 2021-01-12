import os
import semantic_version as sv


def format_ver(ver):
    formattedVer = ""
    for i in range(len(ver)):
        if ver[i] == "_":
            formattedVer += "-"
        else:
            formattedVer += ver[i]
    return formattedVer


def list_pkgdir(pkgDir):
    pkgs = os.listdir(pkgDir)
    pkgname = ""
    ver = ""
    pkgname_ver = {}
    for pkg in pkgs:
        # pkgid+"-"+pkgname+"-"+ver+"-"+verRel+"."+pkgArch+fileExtension
        # 待特殊处理的软件包：cri-tools
        # <软件包哈希>-cri-tools-<版本>-<后缀>
        if "cri-tools" in pkg:
            pkgname = "cri-tools"
            _, _, _, ver, _ = pkg.split("-", 4)
        else:
            _, pkgname, ver, _ = pkg.split("-", 3)
        ver = format_ver(ver)
        if pkgname in pkgname_ver and sv.Version(ver) > sv.Version(pkgname_ver[pkgname]) or pkgname not in pkgname_ver:
            pkgname_ver[pkgname] = ver
    return pkgname_ver
