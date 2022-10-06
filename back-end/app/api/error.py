from flask import jsonify
from werkzeug.http import HTTP_STATUS_CODES

# 为了能在蓝图中返回相应的错误信息,需要蓝图信息和数据库信息
from app.api import bp
from app import db


# 自定义的 基本 错误返回格式，返回的是一个json格式，该函数一般可以被修饰 status_code是由上层传递的网页状态参数
def error_response(status_code, message=None):
    payload = {'error': HTTP_STATUS_CODES.get(status_code, 'Unknown error')}
    if message:
        payload['message'] = message
    # reponse得是json格式
    response = jsonify(payload)
    response.status_code = status_code
    return response


# 这个调用了上面的代码 400:错误的请求
def bad_request(message):
    '''
        message是错误反馈短语
        最常用的错误 400：错误的请求
        返回的是json格式
    '''
    return error_response(400, message)


# errorhandler捕捉当前app或蓝图的状态码，并进行自定制处理
# bp是一个蓝图，发生404、500错误时，返回对应的404、500错误页面
# 404:找不到资源
@bp.app_errorhandler(404)
def not_found_error(error):
    return error_response(404)


# 404:请求被打断
@bp.app_errorhandler(500)
def internal_error(error):
    db.session.rollback()  # 加入数据库commit提交失败，必须回滚
    return error_response(500)
