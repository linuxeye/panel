import os
import sys
from libs import public
path_of_current_file = os.path.abspath(__file__)
path_of_current_dir = os.path.split(path_of_current_file)[0]
_file_name = os.path.basename(__file__)
sys.path.insert(0, path_of_current_dir)
workers = 1
threads = 1
backlog = 512
daemon = True
timeout = 30
bind = "%s:%s" % ("0.0.0.0", public.readfile('data/port.conf'))
worker_class = 'gevent'
chdir = path_of_current_dir 
capture_output = True
access_log_format = '%(t)s %(p)s %(h)s "%(r)s" %(s)s %(L)s %(b)s %(f)s" "%(a)s"'
loglevel = 'info'
pidfile = '%s/logs/%s.pid' % (path_of_current_dir, _file_name)
errorlog = '%s/logs/%s_error.log' % (path_of_current_dir, _file_name)
accesslog = '%s/logs/%s_access.log' % (path_of_current_dir, _file_name)
