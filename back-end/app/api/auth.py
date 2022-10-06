from flask import g
from flask_httpauth import HTTPBasicAuth, HTTPTokenAuth  # api认证,token认证
from app.models import User
from app.api.error import error_response

# enable auth
basic_auth = HTTPBasicAuth()
# enable token
token_auth = HTTPTokenAuth()


# 验证密码，可以自定义验证逻辑
@basic_auth.verify_password
def verify_password(username, password):
    '''用于检查用户提供的用户名和密码'''
    user = User.query.filter_by(username=username).first()
    if user is None:
        return False
    g.current_user = user  # 全局添加一个 User对象属性
    # 检查密钥是否正确
    return user.check_password(password)


@basic_auth.error_handler
def basic_auth_error():
    '''用于在账户密码认证失败的情况下返回错误响应'''
    return error_response(401)


# 后来的登录就可以直接去访问是否有token了，这里也是需要修饰器来修饰
@token_auth.verify_token
def verify_token(token):
    '''用于检查用户请求是否有token，并且token真实存在，且还在有效期内'''
    g.current_user = User.check_token(token) if token else None
    return g.current_user is not None


@token_auth.error_handler
def basic_auth_error():
    '''用于在token认证失败的情况下返回错误响应'''
    return error_response(401)
