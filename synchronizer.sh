#!/bin/bash

# Docker镜像
DOCKER_OR_KUBERNETES="docker"
# 暂时限制成从阿里云同步x86_64架构CentOS下的稳定软件包
LINUX_DISTRIBUTION="centos"
LINUX_DISTRIBUTION_ARCHITECTURE="x86_64"
DOCKER_SOURCE="aliyun"
DOCKER_BRANCH="stable"
# 分别同步CentOS 7和CentOS 8的镜像
# CentOS 7.0-7.9均映射至这个目录
LINUX_DISTRIBUTION_VERSION="7" python docker_and_kubernetes_mirror_synchronizer/sync_controller.py
# CentOS 8.0-8.9均映射至这个目录
LINUX_DISTRIBUTION_VERSION="8" python docker_and_kubernetes_mirror_synchronizer/sync_controller.py

# Kubernetes镜像
DOCKER_OR_KUBERNETES="kubernetes"
KUBERNETES_SOURCE="aliyun"
python docker_and_kubernetes_mirror_synchronizer/sync_controller.py