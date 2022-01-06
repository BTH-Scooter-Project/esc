"""Gunicorn (python web server) config file.

Gunicorn https://gunicorn.org 'Green Unicorn' is a Python WSGI HTTP Server for UNIX.
It's a pre-fork worker model.
The Gunicorn server is broadly compatible with various web frameworks, simply implemented,
light on server resources, and fairly speedy.
"""


bind = "0.0.0.0:8000"
certfile = "ssl/cert/esc_cert.pem"
keyfile = "ssl/cert/esc_key.pem"
workers = 1
# threads = 4
wsgi_app = "project:app"
log_level = "info"
log_file = "/code/logs/gunicorn.log"
accesslog = 'accesslog'
access_logfile = "/code/logs/gunicorn-access.log"
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s"'
