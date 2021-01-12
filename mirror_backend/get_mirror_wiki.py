'''
GET <镜像站URL>/mirrors/<某个指定镜像名>
这份代码把指定镜像的相关信息交给前端，需要返回字段见file://./yaml_templates/mirror_wiki.yaml
'''
from flask import Flask
from flask.json import jsonify
from pkgname_ver_gen import list_pkgdir

app = Flask(__name__)


@app.route("/mirrors/kubernetes")
def gen_pkgname_ver():
    pkgDir = "/var/local_repo/kubernetes/yum/repos/kubernetes-el7-x86_64/Packages/"
    pkgname_ver = list_pkgdir(pkgDir)
    return jsonify({"name": "Kubernetes(k8s)", "count_of_pkgname": len(pkgname_ver), "pkgname_ver": pkgname_ver})


if __name__ == "__main__":
    app.run()
