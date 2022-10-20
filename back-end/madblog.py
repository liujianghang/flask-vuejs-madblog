from app import create_app, db
from app.models import User

app = create_app()


# 配置 Flask Shell 上下文环境, 目的是启动一个Python解释器包含应用的上下文
# 只有应用实例是默认导入的，如果需要导入其他对象，使用shell_context_processor装饰函数，
# 键值对表示额外导入的对象。
@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User}
