from flask import Blueprint

# api是模块名
bp = Blueprint('api', __name__)

# 写在最后是为了防止循环导入，ping.py文件也会导入 bp
# 以下是关于各个模块 导入到bp当中
from app.api import ping, users, tokens