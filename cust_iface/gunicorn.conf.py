"""Gunicorn (python web server) config file.

Gunicorn https://gunicorn.org 'Green Unicorn' is a Python WSGI HTTP Server for UNIX.
It's a pre-fork worker model.
The Gunicorn server is broadly compatible with various web frameworks, simply implemented,
light on server resources, and fairly speedy.
"""


bind = "127.0.0.1:8000"
certfile = "ssl/cert/esc_cert.pem"
keyfile = "ssl/cert/esc_key.pem"
workers = 1
# threads = 4
wsgi_app = "project:app"
