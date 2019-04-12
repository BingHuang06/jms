# 安装
***

### 安装系统依赖环境(centos 7)
    yum -y install mariadb-devel gcc python36 python36-devel python36-pip

### 一般需要更新pip工具
    pip3 install --upgrade pip

### 安装python依赖环境
    pip install -r ./pkgs.txt

### 修改文件权限
    chmod o+wt ./logs
    chmod +x ./init.sh

## 配置数据库(仅支持mysql)
### 创建数据库，创建授权用户
    CREATE DATABASE `jms` CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;
    grant all on jms.* to "jms"@"%" identified by "jmspass";
    grant all on jms.* to "jms"@"localhost" identified by "jmspass";
    grant all on jms.* to "jms"@"127.0.0.1" identified by "jmspass";


### 修改 jms.ini 文件
    [DEFAULT]

    [mysql]
    DBNAME = jms
    USER = jms
    PASSWORD = jmspass
    HOST = 127.0.0.1
    PORT = 3306

### 同步数据库
    python3 ./jumpserver/manage.py migrate

### 创建管理员账号(账号admin，不可自定义)
    python3 createsuperuser.py "adminpass" "admin@jms.com" "管理员"

# 运行
***
    python3 ./jumpserver/manage.py runserver 0.0.0.0:8000


# 部署前端代码至 nginx，配置后端代理
***
## 配置举例

    server {
        listen 80;
        root "/opt/jms/html";

        ...

        location /api/ {
            proxy_pass "http://127.0.0.1:8000/";
        }
    }

