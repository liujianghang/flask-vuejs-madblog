from flask import request, jsonify, Response
from app.api import bp



message = {
    'message1': 'what',
    'message2': 'is',
    'message3': 'it?',
}

@bp.route('/test', methods=['POST'])
def test():
    '''前端Vue.js用来测试与后端Flask API的连通性'''

    print(request.data)
    return jsonify(message)