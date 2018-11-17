# panel
A powerful OneinStack Control Panel
## 环境
Python 3.6</br>
Django 2
## 一期规划:
```
导航       URL          功能
仪表盘     dashboard	展示，服务器运行状况（cpu、内存、磁盘、网卡）
网站       website      站点设置
FTP        ftp          ftp新增删除修改等
数据库     database     数据库添加删除等
计划任务   crontab      设置计划任务
面板设置   setting      面板端口，用户名、密码修改
```
## 安装依赖
```
cd ~/panel
/usr/local/python/bin/pip install -r requirements.txt
```
## 初始化数据库
```
/usr/local/python/bin/python manage.py makemigrations
/usr/local/python/bin/python manage.py migrate
```
## 启动
```
cd ~/panel
/usr/local/python/bin/gunicorn -c runconfig.py panel.wsgi:application
```
