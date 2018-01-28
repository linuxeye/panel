"""
Get install path
"""
import os
from django.conf import settings
OPTIONS = {}
with open(settings.OPTIONS_FILE, 'r') as f:
    for line in f.readlines():
        line = line.strip()
        if not len(line) or line.startswith('#'):
            continue
        OPTIONS[line.split('=')[0]]=line.split('=')[1]
        if line.split('=')[0] in ('mysql_install_dir','mariadb_install_dir','percona_install_dir','alisql_install_dir'):
            if os.path.isdir(line.split('=')[1]+'/support-files'):
                OPTIONS['db_install_dir'] = line.split('=')[1] 
        if line.split('=')[0] in ('mysql_data_dir','mariadb_data_dir','percona_data_dir','alisql_data_dir'):
            if os.path.isfile(line.split('=')[1]+'/mysql-bin.index'):
                OPTIONS['db_data_dir'] = line.split('=')[1] 
        if line.split('=')[0] in ('nginx_install_dir','tengine_install_dir'):
            if os.path.isfile(line.split('=')[1]+'/sbin/nginx'):
                OPTIONS['web_install_dir'] = line.split('=')[1] 
        if line.split('=')[0] == 'openresty_install_dir':
            if os.path.isfile(line.split('=')[1]+'/nginx/sbin/nginx'):
                OPTIONS['web_install_dir'] = line.split('=')[1]+'/nginx' 

print(OPTIONS)
print(OPTIONS['db_install_dir'])
print(OPTIONS['db_data_dir'])
print(OPTIONS['web_install_dir'])
