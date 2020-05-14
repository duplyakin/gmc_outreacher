pidfile = 'o24-prod.pid'
worker_tmp_dir = '/dev/shm'
worker_class = 'gthread'
workers = 4
worker_connections = 1000
timeout = 30
keepalive = 2
threads = 4
proc_name = 'o24-prod'
bind = '0.0.0.0:5050'
backlog = 2048
accesslog = '-'
errorlog = '-'
user = 'o24user'
group = 'o24user'
