#!/bin/sh
/usr/local/share/python2.7/bin/uwsgi --http 127.0.0.1:8001 --chdir /opt/nginx/html/task_manger --home=/usr/local/share/python2.7/ --wsgi-file=wsgi.py -d access.log
