import redis

pool = redis.ConnectionPool(host='localhost', port=6379)
redis_obj = redis.Redis(connection_pool=pool)

# 分页每页做大值
PER_PAGE_MAX_NUM = 10

# css 版本
CSS_VERSION = '201912222145'

SQLALCHEMY_ECHO = False

SQLALCHEMY_ENCODING = 'utf-8'

# 该配置为True,则每次请求结束都会自动commit数据库的变动
SQLALCHEMY_TRACK_MODIFICATIONS = False

# session必须要设置key
# SECRET_KEY = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'

# 限制文件上传大小
MAX_CONTENT_LENGTH = 100 * 1024 * 1024

server_list = {
    'development': {
        'port': '5000',
        'ip': '127.0.0.1',
        'url': 'http://127.0.0.1:5000',
        'debug': True,
        'mysql_password': ''
    },
    'production': {
        'port': '80',
        'ip': 'www.exp1727.cn',
        'url': 'http://www.exp1727.cn:80',
        'debug': False,
        'mysql_password': 'root'
    },
    'test': {
        'port': '8099',
        'ip': 'www.exp1727.cn',
        'url': 'http://www.exp1727.cn:8099',
        'debug': True,
        'mysql_password': 'root'
    }
}

ENV_NAME = 'development'
SERVER_PORT = server_list[ENV_NAME]['port']
IP = server_list[ENV_NAME]['ip']
URL = server_list[ENV_NAME]['url']

DEBUG = server_list[ENV_NAME]['debug']

# mysql数据库连接信息
DIALECT = 'mysql'
DRIVER = 'pymysql'
USERNAME = 'root'
PASSWORD = server_list[ENV_NAME]['mysql_password']
HOST = 'localhost'
PORT = '3306'
DATABASE = 'note'
# 这个连接字符串变量名是固定的具体 参考 flask_sqlalchemy 文档 sqlalchemy会自动找到flask配置中的 这个变量
SQLALCHEMY_DATABASE_URI = '{}+{}://{}:{}@{}:{}/{}?charset=utf8'.format(DIALECT, DRIVER, USERNAME, PASSWORD, HOST, PORT,
                                                                       DATABASE)
