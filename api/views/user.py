from flask import Blueprint, request, make_response, jsonify
#from api.models import User, UserSchema
import json

# ルーティング設定
user_router = Blueprint('user_router', __name__)

# パスとHTTPメソッドを指定
@user_router.route('/users', methods=['GET'])
def get_user_list():
  return make_response(jsonify({ #この値を返す予定
    'users': [
       {
         'id': 1,
         'name': 'John'
       }
     ]
  }))

