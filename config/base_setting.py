import os

# pool = redis.ConnectionPool(host='localhost', port=6379)
# redis_obj = redis.Redis(connection_pool=pool)

# 分页每页做大值
PER_PAGE_MAX_NUM = 10

# css 版本
CSS_VERSION = '2019122231106'

# 打印sql信息
SQLALCHEMY_ECHO = False

SQLALCHEMY_ENCODING = 'utf-8'

# 该配置为True,则每次请求结束都会自动commit数据库的变动
SQLALCHEMY_TRACK_MODIFICATIONS = False

# session必须要设置key
SECRET_KEY = os.urandom(24)

# 限制文件上传大小
MAX_CONTENT_LENGTH = 100 * 1024 * 1024

CELERY_RESULT_BACKEND = 'redis://localhost:6379'
CELERY_BROKER_URL = 'redis://localhost:6379'

server_list = {
    'development': {
        'port': '8008',
        'ip': '0.0.0.0',
        'url': 'http://127.0.0.1:8008',
        'debug': True,
        'mysql_password': '123456'
    },
    'production': {
        'port': '80',
        'ip': 'www.exp1727.cn',
        'url': 'http://www.exp1727.cn:80',
        'debug': False,
        'mysql_password': '123456'
    },
    'tests': {
        'port': '8099',
        'ip': 'www.exp1727.cn',
        'url': 'http://www.exp1727.cn:8099',
        'debug': True,
        'mysql_password': '123456'
    }
}

ENV_NAME = 'development'
SERVER_PORT = server_list[ENV_NAME]['port']
IP = server_list[ENV_NAME]['ip']
URL = server_list[ENV_NAME]['url']
DEBUG = server_list[ENV_NAME]['debug']

# mysql数据库连接信息
DIALECT = 'mysql'
DRIVER = 'mysqlconnector'
USERNAME = 'root'
PASSWORD = server_list[ENV_NAME]['mysql_password']
HOST = '127.0.0.1'
PORT = 3306
DATABASE = 'note'
CHARSET = 'utf8mb4'
# 这个连接字符串变量名是固定的具体 参考 flask_sqlalchemy 文档 sqlalchemy会自动找到flask配置中的 这个变量
SQLALCHEMY_DATABASE_URI = '{}+{}://{}:{}@{}:{}/{}?charset={}'.format(DIALECT, DRIVER, USERNAME, PASSWORD, HOST, PORT,
                                                                     DATABASE, CHARSET)

# 邮件发送配置
MAIL_SERVER = 'smtp.sendgrid.net'
MAIL_PORT = 587
MAIL_USE_TLS = False
MAIL_USERNAME = 'apikey'
MAIL_PASSWORD = os.getenv('SENDGRID_API_KEY')  # 需要去邮箱页面设置里获取
