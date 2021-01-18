#!/bin/bash

set -x

## 暂时解除localhost:8080的访问认证
sed -i 's#\(insecure-port=\).*#\18080#g' /etc/kubernetes/manifests/kube-apiserver.yaml
systemctl restart kubelet

sleep 60

## 正常启动coredns
kubectl create -f https://docs.projectcalico.org/manifests/tigera-operator.yaml
kubectl create -f https://docs.projectcalico.org/manifests/custom-resources.yaml
kubectl get installations.operator.tigera.io default -o yaml | sed 's#\(cidr: \).*#\1172.32.0.0/16#g' | kubectl replace -f -

## 恢复localhost:8080的访问认证
sed -i 's#\(insecure-port=\).*#\10#g' /etc/kubernetes/manifests/kube-apiserver.yaml
systemctl restart kubelet

## 打印镜像列表，完成安装
echo "All pods are as follows:"
kubectl get pod -A -o wide

## TODO 安装dashboard和octant