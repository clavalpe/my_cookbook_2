# type: ignore

bind = "0.0.0.0:8000"
workers = 2
timeout = 120
name = "my_cookbook"
errorlog = "-"
loglevel = "debug"
accesslog = "-"
access_log_format = '%(t)s "%(r)s" %(l)s %(q)s %(s)s "%(f)s" %(u)s "%(a)s"'
