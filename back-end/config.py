import os
from dotenv import load_dotenv


# python中使用python-dotenv这个包来读取环境变量信息
basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))


class Config(object):
    # os.environ.get:取环境变量
    # SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
    #     'sqlite:///' + os.path.join(basedir, 'app.db')

    # 数据库的配置信息
    HOSTNAME = "127.0.0.1"
    PORT = "3306"
    DATABASE = "flask-vuejs-madblog"
    USERNAME = "root"
    PASSWORD = "root"
    DB_URI = "mysql+pymysql://{}:{}@{}:{}/{}?charset=utf8".format(
        USERNAME, PASSWORD, HOSTNAME, PORT, DATABASE
    )
    SQLALCHEMY_DATABASE_URI = DB_URI
    # 减少修改数据库时的内存消耗
    SQLALCHEMY_TRACK_MODIFICATIONS = False