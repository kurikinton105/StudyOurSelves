from flask import Flask, make_response, jsonify
from .views.user import user_router

def create_app():

  api_app = Flask(__name__)
  api_app.register_blueprint(user_router, url_prefix='/api')

  return api_app

api_app = create_app()