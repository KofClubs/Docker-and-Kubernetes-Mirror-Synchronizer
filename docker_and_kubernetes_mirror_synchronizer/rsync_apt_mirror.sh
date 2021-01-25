# 从清华大学开源软件镜像站同步Docker-CE镜像
mkdir -p /var/local_repo/docker-ce/linux/ubuntu/
rsync -av rsync://mirrors.tuna.tsinghua.edu.cn/docker-ce/linux/ubuntu/ /var/local_repo/docker-ce/linux/ubuntu/

# 从清华大学开源软件镜像站同步Kubernetes镜像
mkdir -p /var/local_repo/kubernetes/apt/
rsync -av rsync://mirrors.tuna.tsinghua.edu.cn/kubernetes/apt/ /var/local_repo/kubernetes/apt/