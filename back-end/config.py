import os
from dotenv import load_dotenv


# python中使用python-dotenv这个包来读取环境变量信息
basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))


class Config(object):
    pass