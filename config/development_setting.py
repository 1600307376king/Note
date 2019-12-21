SERVER_PORT = '5000'
IP = '127.0.0.1'
URL = 'http://' + IP + ':' + SERVER_PORT

DEBUG = True

# mysql数据库连接信息
DIALECT = 'mysql'
DRIVER = 'pymysql'
USERNAME = 'root'
PASSWORD = ''
HOST = 'localhost'
PORT = '3306'
DATABASE = 'note'
# 这个连接字符串变量名是固定的具体 参考 flask_sqlalchemy 文档 sqlalchemy会自动找到flask配置中的 这个变量
SQLALCHEMY_DATABASE_URI = '{}+{}://{}:{}@{}:{}/{}?charset=utf8'.format(DIALECT, DRIVER, USERNAME, PASSWORD, HOST, PORT,
                                                                       DATABASE)
