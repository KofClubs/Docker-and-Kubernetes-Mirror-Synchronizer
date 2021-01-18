FROM centos:7

MAINTAINER Zhang Zhanpeng <zhangzp16@outlook.com>

RUN yum install -y python3 python3-pip && \
    yum clean all

RUN pip3 install --no-cache-dir flask && \
    mkdir /usr/src/app

COPY . /usr/src/app

WORKDIR /usr/src/app

CMD ["python3","sync_controller.py"]