#!/bin/bash

mv /etc/nginx/nginx.conf /etc/nginx/nginx.conf.bak
cp nginx.conf /etc/nginx/
systemctl restart nginx