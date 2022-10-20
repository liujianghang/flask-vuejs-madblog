'''
    以下是关于用户操作的部分
'''

import re  # 提供 Perl 风格的正则表达式模式
from flask import request, jsonify, url_for
from app import db
from app.api import bp
from app.api.auth import token_auth  # 所有除了create_user()之外的所有api视图函数都需要添加@token_auth.login_required修饰器验证
from app.api.error import bad_request
from app.models import User


@bp.route('/users', methods=['POST'])
def create_user():
    '''注册一个新用户'''
    # 检查
    data = request.get_json()
    if not data:
        return bad_request('You must post a JSON data.')
    message = {}
    if 'username' not in data or not data.get('username', None):
        message['username'] = 'Please provide a valid username.'
    pattern = '^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$'
    if 'email' not in data or not re.match(pattern, data.get('email', None)):
        message['email'] = 'Please provide a valid email address.'
    if 'password' not in data or not data.get('password', None):
        message['password'] = 'Please provide a valid password.'
    '''核对'''
    if User.query.filter_by(username=data.get('username', None)).first():
        message['username'] = 'Please use a different username.'
    if User.query.filter_by(email=data.get('email', None)).first():
        message['email'] = 'Please use a different email address.'
    if message:
        return bad_request(message)
    '''校验通过，创建用户'''
    user = User()
    user.from_dict(data, new_user=True)  # 设置该对象的数据属性
    db.session.add(user)  # 添加数据
    db.session.commit()  # 提交数据
    response = jsonify(user.to_dict())  # 将对象信息转为json格式
    '''# HTTP协议要求201响应包含一个值为新资源URL的 Location头部(以id添加了一个新的链接)'''
    response.headers['Location'] = url_for('api.get_user', id=user.id)
    return response


@bp.route('/users', methods=['GET'])
@token_auth.login_required
def get_users():
    '''返回所有用户的集合, 这里是分页返回
    这里我们使用了 get() 方法。 它不会调用失败。如果字典的键不存在，
    就会返回一个缺省值（这里是 1 ）。 更进一步它还会把值转换为指定的格式（这里是 int ）
    '''
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 10, type=int), 100)
    # 获取全部的数据
    data = User.to_collection_dict(User.query, page, per_page, 'api.get_users')
    return jsonify(data)


@bp.route('/users/<int:id>', methods=['GET'])
@token_auth.login_required
def get_user(id):
    '''返回一个用户,这里可以看到必须要把得到的User对象转为json格式才可以返回'''
    return jsonify(User.query.get_or_404(id).to_dict())


@bp.route('/users/<int:id>', methods=['PUT'])
@token_auth.login_required
def update_user(id):
    '''修改一个用户'''
    # 请求错误
    user = User.query.get_or_404(id)
    data = request.get_json()
    if not data:
        return bad_request('You must post JSON data.')
    # 校验
    message = {}
    if 'username' in data and not data.get('username', None):
        message['username'] = 'Please provide a valid username.'
    pattern = '^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$'
    if 'email' in data and not re.match(pattern, data.get('email', None)):
        message['email'] = 'Please provide a valid email address.'
    if 'username' in data and data['username'] != user.username and \
            User.query.filter_by(username=data['username']).first():
        message['username'] = 'Please use a different username.'
    if 'email' in data and data['email'] != user.email and \
            User.query.filter_by(email=data['email']).first():
        message['email'] = 'Please use a different email address.'
    # 如果存在错误信息
    if message:
        return bad_request(message)
    # 载入实例对象的新信息 提交到数据库，返回其字典格式
    user.from_dict(data, new_user=False)
    db.session.commit()
    return jsonify(user.to_dict())


@bp.route('/users/<int:id>', methods=['DELETE'])
@token_auth.login_required
def delete_user(id):
    '''删除一个用户'''
    pass
