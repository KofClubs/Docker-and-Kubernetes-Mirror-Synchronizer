#!/bin/bash

set -ex

## 检查用户权限，这个脚本要求root权限
# TODO 最好通过UID校验用户权限，在虚拟机出现误报
# user="$(id -un 2>/dev/null || true)"
# if [ "$user" = 'root' ]; then
#     echo "User permission check OK."
# else
#     echo "You are not root, please press Ctrl+C to abort..."
#     exit 1
# fi

## 检查操作系统发行版
# TODO

## 检查时钟
# TODO

## 关闭全体交换设备
echo "Turning off all swap space..." # TODO 每步操作给一个编号
swapoff -a

## 生成配置文件，配置bridge网络
echo "Writing the following to file:///etc/sysctl.d/k8s.conf..."
if [ ! -d "/etc/sysctl.d" ]; then
    mkdir -p /etc/sysctl.d
fi
cat <<EOF | tee /etc/sysctl.d/k8s.conf
net.bridge.bridge-nf-call-iptables = 1
net.bridge.bridge-nf-call-ip6tables = 1
EOF

## 读取全体内核运行参数
sysctl --system

## 关闭防火墙
echo "Turning off firewall..."
systemctl stop firewalld
systemctl disable firewalld

## 关闭SELinux
echo "Configuring selinux level to permissive..."
setenforce 0
sed -i 's/^SELINUX=enforcing$/SELINUX=permissive/' /etc/selinux/config

## 安装、配置和启动docker（服务）
# TODO 通过包管理器安装docker？
# TODO 前面的校验是否实际无效？
echo "Installing docker from DaoCloud..."
#curl -sSL https://get.daocloud.io/docker | sh
sh docker-ce-installer.sh

# 这里暂时无法写入
echo "Writing the following to file:///etc/docker/daemon.json..."
if [ ! -d "/etc/docker" ]; then
    mkdir -p /etc/docker
fi
cat <<EOF | tee /etc/docker/daemon.json
{
  "exec-opts": ["native.cgroupdriver=systemd"],
  "log-driver": "json-file",
  "log-opts": {
      "max-size": "100m"
  },
  "storage-driver": "overlay2",
  "storage-opts": [
      "overlay2.override_kernel_check=true"
  ]
}
EOF

echo "Turning on or restarting docker service..."
systemctl restart docker
# TODO 测试docker是否已经被正确地安装、配置和启动