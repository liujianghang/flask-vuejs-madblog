# 添加一条路由，以便客户端在需要token时候调用
from flask import jsonify, g
from app import db
from app.api import bp
from app.api.auth import basic_auth


# 调用get_token()函数的时候会指示Flask-HTTPAuth验证身份

# 装饰器 @basic_auth.login_required 将指示 Flask-HTTPAuth 验证身份，当通过 Basic Auth 验证后，才使用用户模型的 get_token()
# 方法来生成 token，数据库提交在生成 token 后发出，以确保 token 及其到期时间被写回到数据库
@bp.route('/tokens', methods=['POST'])
@basic_auth.login_required
def get_token():
    token = g.current_user.get_token() # 在数据库中添加本实例对象
    db.session.commit() # 在这里提交
    return jsonify({'token': token})

@bp.route('/tokens', methods=['DELETE'])
@basic_auth.login_required
def revoke_token():
    g.current_user.revoke_token() # 撤销token
    db.session.commit() # 修改数据库
    return '', 204