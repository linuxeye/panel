# panel
A powerful OneinStack Control Panel
## 一期规划:
```
导航       URL          功能
首页       home         展示，服务器运行状况（cpu、内存、磁盘、网卡）
网站       web          站点设置
FTP       ftp          ftp新增删除修改等
数据库     database     数据库添加删除等
计划任务   crontab      设置计划任务
面板设置   setting      面板端口，用户名、密码修改
```
## 安装依赖
```
/usr/local/python/bin/pip install -r requirements.txt
```
## 初始化数据库
```
/usr/local/python/bin/python manage.py makemigrations
/usr/local/python/bin/python manage.py migrate
```
## 启动
```
/usr/local/python/bin/python manage.py runserver 0.0.0.0:8000
```
