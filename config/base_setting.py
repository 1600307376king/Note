import redis

pool = redis.ConnectionPool(host='localhost', port=6379)
redis_obj = redis.Redis(connection_pool=pool)

SERVER_PORT = '5000'
IP = '127.0.0.1'
URL = 'http://' + IP + ':' + SERVER_PORT
DEBUG = False
SQLALCHEMY_ECHO = False

SQLALCHEMY_ENCODING = 'utf-8'

# 该配置为True,则每次请求结束都会自动commit数据库的变动
SQLALCHEMY_TRACK_MODIFICATIONS = False

# session必须要设置key
SECRET_KEY = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'

# 限制文件上传大小
MAX_CONTENT_LENGTH = 100 * 1024 * 1024

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

SQLALCHEMY_POOL_SIZE = 10000
SQLALCHEMY_MAX_OVERFLOW = 500
