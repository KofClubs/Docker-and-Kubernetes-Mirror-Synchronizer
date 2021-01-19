#!/bin/bash

# 1. 在 /etc/hosts 添加 “10.6.20.1 localhost”
echo '10.6.20.1 localhost'>>/etc/hosts

# 2. 在 /etc/docker/daemon.json 添加 "insecure-registries": [ "0.0.0.0/0" ]
cat <<EOF > /etc/docker/daemon.json
{
  "insecure-registries": [
    "0.0.0.0/0"
  ],
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

# 3. 重启docker
systemctl restart docker