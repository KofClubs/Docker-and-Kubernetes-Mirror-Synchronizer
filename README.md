# Docker-and-Kubernetes-Mirror-Synchronizer

这个同步器可以帮助你搭建Docker和Kubernetes镜像站。

## 使用方法

1. 你可以在指定用户环境变量后执行sync_controller。目前支持增量同步CentOS7 & 8下Docker-CE软件包增量同步和CentOS下Kubernetes软件包。
2. 直接执行synchronizer.sh一次性同步全体支持的软件包。

## 数据接口说明
1. sync_controller执行完后访问`127.0.0.1:5000/mirrors/sync_status`，获得最新同步时间戳和状态；
2. 执行get_mirrors，随时查询本地存储状态，获得软件包归集信息，访问`127.0.0.1:5000/mirrors`，获得软件包大类信息；
3. 执行get_mirror_wiki，对指定仓库，例如Kubernetes，访问`127.0.0.1:5000/mirrors/kubernetes`，获得软件包分类信息。

## 容器化部署
1. sync_controller的容器化部署：`docker run -it -v /var/local_repo:/var/local_repo -p 5000:5000 <容器名> /bin/bash`

## Kubernetes软件包下载、安装和配置

```dotnetcli
cat <<EOF > /etc/yum.repos.d/kubernetes.repo
[kubernetes]
name=Kubernetes
baseurl=https://mirrors.daocloud.io/kubernetes/yum/repos/kubernetes-el7-x86_64/
enabled=1
gpgcheck=0
EOF
setenforce 0
yum install -y kubelet kubeadm kubectl
systemctl enable kubelet && systemctl start kubelet
```