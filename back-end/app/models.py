from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask import url_for
# 给User数据模型中添加token
import base64  # 一种常见的二进制编码方式
from datetime import datetime, timedelta  # 时间对象和时间差对象
import os


# 一个通用类，作用暂时不知道
# API 中有 POST /users 需要返回用户集合，所以还需要添加 to_collection_dict 方法。
# 考虑到后续会创建 Post 等数据模型，所以在 app/models.py 中设计一个通用类 PaginatedAPIMixin
# PaginatedAPIMixin:分页混合的api 这里是返回集合的固定写法
class PaginatedAPIMixin(object):
    @staticmethod
    def to_collection_dict(query, page, per_page, endpoint, **kwargs):
        resources = query.paginate(page, per_page, False)
        data = {
            'items': [item.to_dict() for item in resources.items],
            '_meta': {
                'page': page,
                'per_page': per_page,
                'total_pages': resources.pages,
                'total_items': resources.total
            },
            '_links': {
                'self': url_for(endpoint, page=page, per_page=per_page,
                                **kwargs),
                'next': url_for(endpoint, page=page + 1, per_page=per_page,
                                **kwargs) if resources.has_next else None,
                'prev': url_for(endpoint, page=page - 1, per_page=per_page,
                                **kwargs) if resources.has_prev else None
            }
        }
        return data


''' 继承了上面的返回的 集合类 '''


class User(PaginatedAPIMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))  # 不保存原始密码
    token = db.Column(db.String(32), index=True, unique=True)  # token密钥
    token_expiration = db.Column(db.DateTime)  # 设定的密钥的过期时间

    # 当打印这个对象的时候，会自动调用这个方法
    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    # 后续调用该方法返回字典，再用 flask.jsonify 将字典转换成 JSON 响应
    def to_dict(self, include_email=False):
        data = {
            'id': self.id,
            'username': self.username,
            '_links': {
                'self': url_for('api.get_user', id=self.id)
            }
        }
        if include_email:
            data['mail'] = self.email
        return data

    # 设置属性函数
    def from_dict(self, data, new_user=False):
        for field in ['username', 'email']:
            if field in data:
                setattr(self, field, data[field])
        if new_user and 'password' in data:
            self.set_password(data['password'])

    # expires_in为给定的过期时间，默认为3600秒
    def get_token(self, expires_in=3600):
        now = datetime.utcnow()  # utcnow是世界时间
        if self.token and self.token_expiration > now + timedelta(seconds=60): # 没有过期的情况
            return self.token # 返回老密钥
        self.token = base64.b64encode(os.urandom(24)).decode('utf-8') # 设置一个新生成的密钥
        self.token_expiration = now + timedelta(seconds=expires_in)
        db.session.add(self) # 在数据库中添加本实例对象
        return self.token

    # 撤销token 直接将token_expiration置为相对于 现在 过去的时间
    def revoke_token(self):
        self.token_expiration = datetime.utcnow() - timedelta(seconds=1)

    # 根据token查看用户
    @staticmethod
    def check_token(token):
        user = User.query.filter_by(token=token).first()
        if user is None or user.token_expiration < datetime.utcnow():
            return None
        return user # 返回这个搜到的对象
