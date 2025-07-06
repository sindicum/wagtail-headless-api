import multiprocessing
import os

# Server socket
bind = "0.0.0.0:8000"
backlog = 2048

# Worker processes
# workers = multiprocessing.cpu_count() * 2 + 1
workers = 2
worker_class = 'sync'
worker_connections = 1000
timeout = 120
keepalive = 2
graceful_timeout = 30

# Performance
max_requests = 1000
max_requests_jitter = 100
preload_app = True
worker_tmp_dir = '/dev/shm'

# Logging
accesslog = '-'
errorlog = '-'
loglevel = 'info'
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s"'

# Process naming
proc_name = 'wagtailheadlessapi_gunicorn'

# Server mechanics
daemon = False
pidfile = None
tmp_upload_dir = None

# Security
limit_request_line = 4094
limit_request_fields = 100
limit_request_field_size = 8190

# SSL/TLS
keyfile = None
certfile = None