#!/bin/bash

set -ex

## 安装、配置和启动k8s
echo "Writing the following to file:///etc/yum.repos.d/kubernetes.repo"
if [ ! -d "/etc/yum.repos.d" ]; then
    mkdir -p /etc/yum.repos.d
fi
cat <<EOF > /etc/yum.repos.d/kubernetes.repo
[kubernetes]
name=Kubernetes
baseurl=http://mirrors.daocloud.io/kubernetes/yum/repos/kubernetes-el7-x86_64/
enabled=1
gpgcheck=0
EOF

echo "Installing docker from official repository..."
yum install -y kubelet kubeadm kubectl --disableexcludes=kubernetes

echo "Configuring file:///usr/lib/systemd/system/kubelet.service.d/10-kubeadm.conf and turning on kubelet..."
systemctl enable --now kubelet
sed -i 's#\(Environment="KUBELET_CONFIG_ARGS=--config=/var/lib/kubelet/config.yaml\).*#\1 --cgroup-driver=systemd"#g' /usr/lib/systemd/system/kubelet.service.d/10-kubeadm.conf

systemctl daemon-reload
systemctl restart kubelet
# systemctl status kubelet
# TODO 测试k8s是否已经被正确地安装、配置和启动

## 把“uid hostname”写入hosts，配置k8s网络
echo "Configuring kubernetes network at file:///etc/hosts..."
echo `ip route get 1 | awk '{print $NF;exit}'` `hostname` >> /etc/hosts
kubeadm init --image-repository 10.6.20.1/gcr_containers --pod-network-cidr 172.32.0.0/16 # 指定pod网络的IP地址范围

## 启用用户级kubernetes设置
echo Enabling user-level configurations at file://$HOME/.kube...
mkdir -p $HOME/.kube
cp -i /etc/kubernetes/admin.conf $HOME/.kube/config
chown $(id -u):$(id -g) $HOME/.kube/config