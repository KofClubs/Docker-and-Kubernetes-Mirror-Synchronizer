'''
GET <镜像站URL>/mirrors
这份代码把镜像分类的信息交给前端，需要返回字段见file://./yaml_templates/mirror_list.yaml
'''
from flask import Flask, Response
import json

app = Flask(__name__)

mirrorIdList = ["dce", "k8s"]
mirrorNameList = ["Docker", "Kubernetes(k8s)"]
latestTagList = ["0.0.0", "0.0.0"]
statusList = ["syncing", "syncing"]
latestSyncTimestampList = ["27182818", "31415926"]
iconList = ["example.com/images/dce.svg", "example.com/images/k8s.svg"]


@app.route("/mirrors")
def list_mirrors():
    resp = []
    global mirrorIdList, mirrorNameList, latestTagList, statusList, latestSyncTimestampList, iconList
    for i in range(len(mirrorIdList)):
        resp.append({"id": mirrorIdList[i], "name": mirrorNameList[i], "latest_tag": latestTagList[i],
                     "status": statusList[i], "timestamp": latestSyncTimestampList[i], "icon": iconList[i]})
    return Response(json.dumps(resp), mimetype='application/json')


if __name__ == "__main__":
    app.run()
