import os
import semantic_version as sv


def format_ver(ver):
    digits = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    formattedVer = ""
    countOfDot = 0  # 我们只返回major.minor.patch格式的版本号
    for i in range(len(ver)):
        if ver[i] not in digits and countOfDot >= 2:
            return formattedVer
        if ver[i] == ".":
            countOfDot += 1
        formattedVer += ver[i]
    return formattedVer


def list_pkgdir(pkgDir):
    pkgs = os.listdir(pkgDir)
    pkgname = ""
    ver = ""
    pkgname_ver = {}
    for pkg in pkgs:
        # pkgid+"-"+pkgname+"-"+ver+"-"+verRel+"."+pkgArch+fileExtension
        # 待特殊处理的软件包：cri-tools kubernetes-cni
        # <软件包哈希>-cri-tools-<版本>-<后缀>
        pkgname = ""
        ver = ""
        countOfDash = pkg.count("-")
        if countOfDash == 3:
            _, pkgname, ver, _ = pkg.split("-", 3)
        elif countOfDash == 4:
            _, pkgname1, pkgname2, ver, _ = pkg.split("-", 4)
            pkgname = pkgname1+"-"+pkgname2
        else:
            print(f"Please check this package filename: {pkg}")

        try:
            ver = format_ver(ver)
        except:
            print(f"{ver} is not a version string.")
        # ver = format_ver(ver)
        else:
            if pkgname in pkgname_ver and sv.Version(ver) > sv.Version(pkgname_ver[pkgname]) or pkgname not in pkgname_ver:
                pkgname_ver[pkgname] = ver
    return pkgname_ver
