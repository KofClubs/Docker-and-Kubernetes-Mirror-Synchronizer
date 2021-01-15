FROM centos:7

MAINTAINER Zhang Zhanpeng <zhangzp16@outlook.com>

RUN yum install -y python3 python3-pip && \
    yum clean all

RUN mkdir /usr/src/app

COPY . /usr/src/app

RUN pip3 install --no-cache-dir flask

CMD ["python3","sync_controller.py"]