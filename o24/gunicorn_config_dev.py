pidfile = '/home/o24user/o24-dev.pid'
worker_tmp_dir = '/dev/shm'
worker_class = 'gthread'
workers = 2
worker_connections = 1000
timeout = 30
keepalive = 2
threads = 4
proc_name = 'o24-dev'
bind = 'unix:/home/o24user/o24-dev.sock'
backlog = 2048
loglevel = 'debug'
accesslog = '/home/o24user/logs/dev/gunicorn_access_log'
acceslogformat ="%(h)s %(l)s %(u)s %(t)s %(r)s %(s)s %(b)s %(f)s %(a)s"
errorlog =  '/home/o24user/logs/dev/gunicorn_error_log'
user = 'o24user'
group = 'o24user'
