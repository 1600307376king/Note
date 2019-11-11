/*
Navicat MySQL Data Transfer

Source Server         : local
Source Server Version : 50505
Source Host           : localhost:3306
Source Database       : note

Target Server Type    : MYSQL
Target Server Version : 50505
File Encoding         : 65001

Date: 2019-11-11 15:35:07
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for notes
-- ----------------------------
DROP TABLE IF EXISTS `notes`;
CREATE TABLE `notes` (
  `n_id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `uuid` varchar(255) DEFAULT NULL,
  `note_title` varchar(255) DEFAULT NULL,
  `note_labels` varchar(255) DEFAULT NULL,
  `note_content` mediumtext DEFAULT NULL,
  `note_instructions` text DEFAULT NULL,
  `creation_time` datetime DEFAULT NULL,
  PRIMARY KEY (`n_id`)
) ENGINE=InnoDB AUTO_INCREMENT=24 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of notes
-- ----------------------------
INSERT INTO `notes` VALUES ('13', '0d6a7f1c-0429-11ea-aaeb-001a7dda7113', 'Apache + flask windows环境搭建', 'Apache |Flask |Windows |', '\n####步骤 1\n* 下载对应版本 Apache mod_wsgi Python\n\n* Apache,mod_wsgi和Python都必须用相同版本的C/C++编译器生成，要么都是32位的，要么都是64位的，不能混用。\n\n* Apache和mod_wsgi 也必须选择相同位数相同VC编译版本（比如：都是x64 VC14编译）\n\n* python flask Apache 下载安装步骤忽略\n\n\n####步骤 2\n* 安装mod_wsgi\n- 下载连接 https://www.lfd.uci.edu/~gohlke/pythonlibs/ 然后选择点击mod_wsgi\n\n- 将下载的文件后缀改为zip，解压出来，拷贝mod_wsgi.cp37-win_amd64.pyd 文件放到C:\\Apache24\\modules 目录，并改名为mod_wsgi.pyd\n\n* 修改 httpd.conf 配置 例Apache配置文件：C:\\Apache24\\conf\\httpd.conf\n- 搜索SRVROOT 并修改apache目录的路径\n\n- 加载mod_wsgi模块，在httpd.conf中找到LoadModule最后一行后面增加行 LoadModule wsgi_module modules/mod_wsgi.pyd\n\n- 修改httpd.conf配置，末尾增加内容：8090端口与apache 监听端口保持一致。\"c:/web\" 为项目路径，以下三个路径保持相同\n\n\n    <VirtualHost *:8090 >\n    ServerAdmin \"0.0.0.0\"\n    DocumentRoot \"c:/web\"\n\n    <Directory \"c:/web\">\n    Require all granted\n    Require host ip\n    Allow from all\n    </Directory>\n    WSGIScriptAlias / c:/web/test.wsgi\n    </VirtualHost>\n\n\n- 继续修改httpd.conf，找到一下内容启用他\n\n\n    LoadModule access_compat_module modules/mod_access_compat.so #基于主机的组授权（名称或IP地址） httpd 2.x兼容的模块，\n    LoadModule proxy_module modules/mod_proxy.so #apache的代理模块\n    LoadModule proxy_http_module modules/mod_proxy_http.so #代理http和https请求\n    LoadModule vhost_alias_module modules/mod_vhost_alias.so #虚拟主机动态配置\n    LoadModule authz_host_module modules/mod_authz_host.so #基于主机的组授权\n    Include conf/extra/httpd-vhosts.conf#启用虚拟主机配置\n\n\n* 创建一个flask 项目 如命名为web\n\n- 新建文件test.wsgi\n\n- 把刚创建的web目录中的app.py 重命名为main.py 也可以不改，添加如下代码(示例)\n\n\n    from flask import Flask\n\n    app = Flask(__name__)\n\n    @app.route(\'/\')\n    def hello_world():\n    return \'Hello World!\'\n\n    @app.route(\"/index/\")\n    def foo():\n    return \"index page\"\n\n\n    @app.route(\"/login/\")\n    def login():\n    return \"login page\"\n\n    if __name__ == \'__main__\':\n    app.run()\n\n- 添加test.wsgi代码 注意 application 不能改变，\"C:/web\"为项目路径，main 为main.py名称\n\n\n    import sys\n\n    sys.path.insert(0, \"C:/web\")\n\n    from main import app\n\n    application = app\n\n#### 步骤 3\n* 最后启动Apache/bin/目录下cmd 命令输入httpd， 浏览器输入localhost:8090 返回hello world就算配置成功\n', '前提条件\n下载对应版本 Apache mod_wsgi Python\nApache,mod_wsgi和Python都必须用相同版本的C/C++编译器生成，要么都是32位的，要么都是64位的，不能混用。\nApache和mod_wsgi 也必须选择相同位数相同VC编译版本（比如：都是x64 VC14编译）\npython flask Apache 下载安装步骤忽略 ', '2019-11-11 10:14:55');
INSERT INTO `notes` VALUES ('14', 'f97e2b26-0432-11ea-bbf3-001a7dda7113', 'flask 后端token验证', 'Flask |Token |', '\n#####1.生成token\n    def generate_token(key, expire=3600):\n        ts_str = str(time.time() + expire)\n        ts_byte = ts_str.encode(\"utf-8\")\n        sha1_tshexstr = hmac.new(key.encode(\"utf-8\"), ts_byte, \'sha1\').hexdigest()\n        token = ts_str + \':\' + sha1_tshexstr\n        b64_token = base64.urlsafe_b64encode(token.encode(\"utf-8\"))\n        return b64_token.decode(\"utf-8\")\n\n#####2.验证token,用户id和token\n    def certify_token(key, token):\n        if key == \'null\':\n            return False\n        token_str = base64.urlsafe_b64decode(token).decode(\'utf-8\')\n        token_list = token_str.split(\':\')\n        if len(token_list) != 2:\n            return False\n        ts_str = token_list[0]\n        if float(ts_str) < time.time():\n            # token expired\n            return False\n        known_sha1_tsstr = token_list[1]\n        sha1 = hmac.new(key.encode(\"utf-8\"), ts_str.encode(\'utf-8\'), \'sha1\')\n        calc_sha1_tsstr = sha1.hexdigest()\n        if calc_sha1_tsstr != known_sha1_tsstr:\n            # token certification failed\n            return False\n            # token certification success\n        return True\n\n#####3.用户登录mysql模型\n    from passlib.apps import custom_app_context as pwd_context\n    from app import db\n\n\n    class User(db.Model):\n        __table_name__ = \'user\'\n        user_id = db.Column(db.INT, primary_key=True)\n        user_name = db.Column(db.String(255))\n        user_password = db.Column(db.String(255))\n\n        def __init__(self, **kwargs):\n            self.user_id = kwargs[\'id_u\']\n            self.user_name = kwargs[\'user_name\']\n            self.user_password = kwargs[\'user_password\']\n\n        def hash_password(self, password):\n            self.user_password = pwd_context.encrypt(password)\n\n        def verify_password(self, password):\n            return pwd_context.verify(password, self.user_password)\n\n#####4.登录模板\n    def login():\n        user_name = request.form.get(\'user_name\')\n        password = request.form.get(\'password\')\n        msg = User.query.filter(User.user_name == user_name).first()\n        if msg\n            if msg.verify_password(password):\n                token = generate_token(str(msg.user_id))\n                return jsonify({\'status\': 200})\n\n\n', 'flask后端token模板', '2019-11-11 11:25:56');
INSERT INTO `notes` VALUES ('15', 'e734ae8c-0444-11ea-9fbd-001a7dda7113', 'cookie 的使用和案例', 'Cookie |', '#### 参考链接https://www.w3school.com.cn/js/js_cookies.asp\n\n##### 1. 基本语法\n######  1.1 方法一\n    # 创建cookie 整个站点可用 name: cookie名称, value: cookie值，expiress: 有效期\n    Cookies.set(\'name\', \'value\'， { expiress:4});\n\n    # 设置有效期15分钟\n    var inFifteenMinutes = new Date(new Date().getTime() + 15 * 60 * 1000);\n    Cookies.set(\'foo\', \'bar\', {\n    expires: inFifteenMinutes\n    });\n\n    # 设置有效路径, 在http://127.0.0.1/path1/路径下cookie有效\n    Cookies.set(\'name\', \'value\', { expires: 4, path: \'/\' });\n    Cookies.set(\'name\', \'value\', { expires: 4, path: \'http://127.0.0.1/path1/xxx.html\' });\n\n    # 读取cookie\n    Cookies.get(\'name\')\n\n    # 读取所有可见cookie：返回的是个json对象；\n    Cookies.get()\n\n    # 删除Cookie\n    Cookies.remove(\'name\')\n    # 删除当前页面所在路径下某个有效的cookie\n    Cookies.set(\'name\', \'value\', { path: \'\' })\n    Cookies.remove(\'name\') // fail!\n    Cookies.remove(\'name\', { path: \'\' }) // removed!\n    # cookie是否编码\n    $.cookie.raw = true;\n\n    # 是否以json格式进行存储和读取\n    $.cookie.json = true;\n\n###### 1.2 方法二\n    # 创建cookie\n    document.cookie = \"username=Bill Gates\";\n\n    # 添加有效日期（UTC 时间）。默认情况下，在浏览器关闭时会删除 cookie\n    document.cookie = \"username=John Doe; expires=Sun, 31 Dec 2017 12:00:00 UTC\";\n\n    # 读取cookie 会在一条字符串中返回所有 cookie，比如：cookie1=value; cookie2=value; cookie3=value\n    var x = document.cookie;\n\n    # 修改cookie\n    document.cookie = \"username=Steve Jobs; expires=Sun, 31 Dec 2017 12:00:00 UTC; path=/\";\n\n    # 删除cookie 直接把 expires 参数设置为过去的日期即可\n    document.cookie = \"username=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;\";\n\n##### 2 封装cookie的增删改查的函数\n    function setCookie(key, value, iDay) {\n        var oDate = new Date();\n        oDate.setDate(oDate.getDate() + iDay);\n        document.cookie = key + \'=\' + value + \';expires=\' + oDate;\n    }\n\n    function removeCookie(key) {\n        setCookie(key, \'\', -1);//这里只需要把Cookie保质期退回一天便可以删除\n        }\n\n        function getCookie(key) {\n            var cookieArr = document.cookie.split(\'; \');\n            for(var i = 0; i < cookieArr.length; i++) {\n                var arr = cookieArr[i].split(\'=\');\n            if(arr[0] === key) {\n                return arr[1];\n            }\n        }\n        return false;\n    }', 'cookie 使用教程', '2019-11-11 13:34:17');
INSERT INTO `notes` VALUES ('16', '2a3f1a9a-044a-11ea-8216-001a7dda7113', '手动创建vue项目命令', 'Vue|', '\n##### 步骤 1\n    vue init webpack my-vue\n    \'my-vue\' 指项目名称\n\n##### 步骤 2 测试运行\n    cd npm run dev\n\n##### 步骤 3 安装项目依赖\n    npm install \n    npm install --registry=https://registry.npm.taobao.org # 利用淘宝镜像加速\n', 'vue创建', '2019-11-11 14:11:57');
INSERT INTO `notes` VALUES ('17', 'd741c5c6-044b-11ea-b36b-001a7dda7113', 'CentOS7.2.1511卸载并重新安装python2.7及yum', 'Centos|Python2|Yum|', '###1.卸载python\n    rpm -qa|grep python|xargs rpm -e --allmatches --nodeps\n    whereis python|xargs rm -fr\n\n###2.卸载yum\n    rpm -qa|grep yum|xargs rpm -e --allmatches --nodeps\n    rm -rf /etc/yum.repos.d/*\n    whereis yum|xargs rm -fr\n\n###3.创建目录python和yum用以存放rpm包\n    mkdir /usr/local/src/python\n    mkdir /usr/local/src/yum\n\n###4.使用wget分别下载python以及yum的rpm包（注意：一定要和系统的版本号对应）\n#####（1）下载python的rpm包\n\n    cd /usr/local/src/python\n    wget http://vault.centos.org/7.2.1511/os/x86_64/Packages/python-2.7.5-34.el7.x86_64.rpm\n    wget http://vault.centos.org/7.2.1511/os/x86_64/Packages/python-iniparse-0.4-9.el7.noarch.rpm\n    wget http://vault.centos.org/7.2.1511/os/x86_64/Packages/python-pycurl-7.19.0-17.el7.x86_64.rpm\n    wget http://vault.centos.org/7.2.1511/os/x86_64/Packages/python-devel-2.7.5-34.el7.x86_64.rpm\n    wget http://vault.centos.org/7.2.1511/os/x86_64/Packages/python-libs-2.7.5-34.el7.x86_64.rpm\n    wget http://vault.centos.org/7.2.1511/os/x86_64/Packages/python-urlgrabber-3.10-7.el7.noarch.rpm\n    wget http://vault.centos.org/7.2.1511/os/x86_64/Packages/rpm-python-4.11.3-17.el7.x86_64.rpm\n\n\n#####（2）下载yum的rpm包\n    cd /usr/local/src/yum        \n    wget http://vault.centos.org/7.2.1511/os/x86_64/Packages/yum-3.4.3-132.el7.centos.0.1.noarch.rpm\n    wget http://vault.centos.org/7.2.1511/os/x86_64/Packages/yum-metadata-parser-1.1.4-10.el7.x86_64.rpm\n    wget http://vault.centos.org/7.2.1511/os/x86_64/Packages/yum-plugin-fastestmirror-1.1.31-34.el7.noarch.rpm\n\n\n###5.安装python以及yum的rpm包\n#####（1）安装python\n    cd /usr/local/src/python\n    rpm -ivh python-*   rpm-python-*\n    # 出现依赖问题使用以下命令\n    rpm -ivh python-*   rpm-python-* --nodeps --force\n    \n#####（2）安装yum\n    cd /usr/local/src/yum \n    rpm -ivh yum-*', '误删centOS7.2自带python2.7 导致yum无法正常使用', '2019-11-11 14:23:56');
INSERT INTO `notes` VALUES ('18', '7bb127a8-044e-11ea-b14b-001a7dda7113', 'docker 的一些使用', 'Docker|Centos|', '## docker hub 账号 docker1996jjc\n##### 1 修改docker存储目录\n    docker info # 查看Docker Root Dir \n    vi /usr/lib/systemd/system/docker.service\n    # 在ExecStart 内添加一下配置，注意不要有多余空格\n    --graph=/home/docker \\ \n    --storage-driver=overlay \\\n    systemctl daemon-reload\n    systemctl restart docker\n\n##### 2 从宿主机复制文件至容器\n    docker cp 文件名 容器ID:目标路径\n\n##### 3 创建虚拟端口的容器 并拥有所有权限\n    docker run -p 8080:80 -d --privileged 容器ID init\n##### 4 将容器保存位镜像\n    docker commit 容器ID 镜像名称\n##### 5 将镜像保存为文件，将文件转化为镜像\n    docker save -o 文件名 镜像ID\n    docker load < 文件名\n\n##### 6 进入容器和退出\n    docker exec -it 容器ID /bin/bash\n    exit', 'docker笔记', '2019-11-11 14:42:51');
INSERT INTO `notes` VALUES ('19', 'b158e608-044e-11ea-8f6e-001a7dda7113', 'Centos7安装mysql5.6教程', 'Centos|Mysql|', '##### 下载mysql的repo源\n    wget http://repo.mysql.com/mysql-community-release-el7-5.noarch.rpm\n##### 安装mysql-community-release-el7-5.noarch.rpm包\n    rpm -ivh mysql-community-release-el7-5.noarch.rpm\n##### 安装mysql\n    yum install mysql-server\n##### 加入开机启动\n    systemctl enable mysqld\n##### 启动mysql服务进程\n    systemctl start mysqld\n##### 重置密码\n    mysql_secure_installation\n##### mysql -u root -p\n    mysql -u root -p', 'mysql 安装教程', '2019-11-11 14:44:21');
INSERT INTO `notes` VALUES ('20', 'f9797a98-044e-11ea-8248-001a7dda7113', 'Nginx 安装教程 ', 'Nginx|Centos|', '### 1. 卸载Nginx\n##### service nginx stop\n##### whereis nginx\n##### rm -rf [所有相关文件]\n##### yum remove nginx\n\n### 2. 安装\n###### 2.1 安装依赖包\n     yum -y install gcc gcc-c++ make libtool zlib zlib-devel openssl openssl-devel pcre pcre-devel\n ##### 2.2 下载源码解压编译\n     wget http://nginx.org/download/nginx-1.17.5.tar.gz\n     tar -zxvf nginx-1.17.5.tar.gz\n     cd nginx-1.17.5\n     ./configure\n     make && make install\n\n## 3. 配置nginx的systemctl命令\n    cd /usr/lib/systemd/system\n    vi nginx.service\n\n ##### 3.1 复制粘贴以下\n    [Unit]\n    Description=The nginx HTTP and reverse proxy server\n    After=network.target remote-fs.target nss-lookup.target\n\n    [Service]\n    Type=forking\n    PIDFile=/usr/local/nginx/logs/nginx.pid\n    ExecStartPre=/usr/local/nginx/sbin/nginx -t -c /usr/local/nginx/conf/nginx.conf\n    ExecStart=/usr/local/nginx/sbin/nginx -c /usr/local/nginx/conf/nginx.conf\n    ExecReload=/usr/local/nginx/sbin/nginx -s reload\n    ExecStop=/usr/local/nginx/sbin/nginx -s stop\n    ExecQuit=/usr/local/nginx/sbin/nginx -s quit\n\n    [Install]\n    WantedBy=multi-user.target\n\n##### 3.2 重启服务\n    systemctl daemon-reload\n##### 4 启动nginx,如无法启动检查端口是否被占用\n    systemctl start nginx.service', 'Nginx 安装教程 在centos7上安装', '2019-11-11 14:46:22');
INSERT INTO `notes` VALUES ('21', 'ebb15f38-044f-11ea-9f87-001a7dda7113', 'centos7.2 安装python3.7', 'Centos|Python|', '###一、安装依赖包\n    yum install zlib-devel bzip2-devel openssl-devel ncurses-devel sqlite-devel readline-devel tk-devel gcc make\n    yum install libffi-devel -y\n\n###二、下载压缩包\n    wget https://www.python.org/ftp/python/3.7.0/Python-3.7.0.tgz\n\n###三、解压、安装Python3.7.0\n    tar -zxvf Python-3.7.0.tgz\n    cd Python-3.7.0\n    ./configure\n    make&&make install\n\n###四、配置环境变量\n    mv /usr/bin/python /usr/bin/python.bak\n    ln -s /usr/local/bin/python3 /usr/bin/python\n    mv /usr/bin/pip /usr/bin/pip.bak\n    ln -s /usr/local/bin/pip3 /usr/bin/pip', 'centos7.2 安装python3.7', '2019-11-11 14:53:09');
INSERT INTO `notes` VALUES ('22', '13d931a2-0450-11ea-b94e-001a7dda7113', '两台linux主机文件传送', 'linux |', '##### 1 scp 命令\n    scp -r 文件名 root@192.168.4.44:目标主机保存路径', '两台linux主机文件传送', '2019-11-11 14:54:16');
INSERT INTO `notes` VALUES ('23', '83835e54-0450-11ea-b891-001a7dda7113', 'uWSGI 配置', 'Uwsgi|Centos|', '#### 1 centos 7.2 环境下\n##### 1.1 Flask 例子\n    #!/usr/bin/python3\n    from flask import Flask\n\n    app = Flask(__name__)\n\n    @app.route(\"/\")\n    def helloWorld():\n    return \"你好\"\n\n    if __name__ == \'__main__\':\n    app.run(host=\'0.0.0.0\', port=8080)\n##### 1.2 创建uswgi.ini 运行 uwsgi --ini uwsgi.ini\n    [uwsgi]\n    socket = 127.0.0.1:8099 # 选择socket时，ip 与 nginx 对应\n    wsgi-file = app.py\n    callable = app  \n    processes = 4\n    threads = 2\n    #daemonize = /var/www/pj/wsgi.log\n\n##### 1.3 修改nginx 配置文件 nginx.conf \n    # 在server 内配置location\n    location / {\n    include uwsgi_params;\n    uwsgi_pass 0.0.0.0:8099; # 与uwsgi.ini 文件内socket 端口对应\n    }', 'uWSGI 配置', '2019-11-11 14:57:23');
