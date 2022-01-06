#!/usr/bin/env bash

mkdir -p /code/logs
touch /code/logs/gunicorn.log
touch /code/logs/gunicorn-access.log
tail -n 0 -f /code/logs/gunicorn*.log &

cd cust_iface
gunicorn &
cd ../
python3 main.py
