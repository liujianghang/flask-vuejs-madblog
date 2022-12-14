from flask import jsonify, g
from app import db
from app.api import bp
from app.api.auth import basic_auth

# 这里调用了/tokens，传递得到账号和密码，就会自动去auth验证账号密码
@bp.route('/tokens', methods=['POST'])
@basic_auth.login_required
def get_token():
    token = g.current_user.get_jwt()
    # 每次用户登录（即成功获取 JWT 后），更新 last_seen 时间
    g.current_user.ping()
    db.session.commit()
    return jsonify({'token': token})