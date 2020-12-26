import os

LINUX_DISTRIBUTION = os.getenv("LINUX_DISTRIBUTION", "centos")
SOURCE = os.getenv("SOURCE", "aliyun")
TESTING_VERSION_PERMISSION = os.getenv("TESTING_VERSION_PERMISSION", False)
VERSION_DEPTH = os.getenv("VERSION_DEPTH", 1)
LOCAL_REPO_DIR = os.getenv(
    "LOCAL_REPO_DIR", "/var/local_repo/kubernetes/yum/repos/kubernetes-el7-x86_64/Packages")
