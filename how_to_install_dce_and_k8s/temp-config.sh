#!/bin/bash

# 1. 在 /etc/hosts 添加 “10.6.20.1 localhost”

# 2. 在 /etc/docker/daemon.json 添加 "insecure-registries": [ "0.0.0.0/0" ]

# 3. 重启docker