#!/bin/bash

gunicorn --certfile=ssl/cert/esc_cert.pem --keyfile=ssl/cert/esc_key.pem --workers=2 --bind=127.0.0.1:8000 project:app

