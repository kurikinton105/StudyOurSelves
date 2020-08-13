from flask import Flask, render_template,request #追加
from flask import Flask
from flask import Flask,flash,redirect,render_template,request,session,abort
import flask , flask_login
from api.views.user import user_router
from flask import Blueprint, request, make_response, jsonify
import json
from api.__init__ import api_app
app = Flask(__name__)

#Login処理の試しを作ってみる
app.secret_key = 'hogehoge'

class User(flask_login.UserMixin):
    pass

login_manager = flask_login.LoginManager()
login_manager.init_app(app)

users = {'example@com': {'password': 'password'}}

@login_manager.user_loader
def user_loader(email):
    if email not in users:
        print("idが違います")
        return

    user = User()
    user.id = email
    return user

@login_manager.request_loader
def request_loader(request):
    email = request.form.get('username')
    if email not in users:
        return

    user = User()
    user.id = email

    # DO NOT ever store passwords in plaintext and always compare password
    # hashes using constant-time comparison!
    user.is_authenticated = request.form['password'] == users[email]['password']

    return user

# ------------------------------------------------------------------
@app.route('/') #はじめに表示！！
def home():
   if not session.get('logged_in'): #ログインしていなかったら表示
       #print("A")
       print("最初のログイン")
       return render_template('index.html')
   else:
       print("ログインなう")
       return render_template('home.html',id_name=flask_login.current_user.id)
# ------------------------------------------------------------------
@app.route('/loginpage')
def showloginpage():
    return render_template('home.html')
#database

@app.route('/login', methods=['POST']) #ここでログインのPOSTを行う
def do_admin_login():
    id_name = flask.request.form['username'] #ユーザーネームの取り出し
    if flask.request.form['password'] == users[id_name]['password']:
        session['logged_in'] = True
        user = User()
        user.id = id_name
        flask_login.login_user(user)
        print("ログインしました。")
        #return home()
        return flask.redirect(flask.url_for('home'))
    else:
        flash('パスワードまたは、ユーザー名が違います。')
        return home()

@app.route('/protected')
@flask_login.login_required #ログインが必要だよ
def protected():
    print(flask_login.current_user.id)
    return render_template('home.html',id_name=flask_login.current_user.id)
    #return 'Logged in as: ' + flask_login.current_user.id

# ------------------------------------------------------------------
@app.route("/logout")
def logout():
   session['logged_in'] = False
   flask_login.logout_user()
   return home()

@app.route('/api', methods=['GET'])
def doc():
    return "<H1>ここにドキュメント</H1>"

@app.route('/api/users', methods=['GET'])
def get_user_list():
  return make_response(jsonify({ #この値を返す予定
    'users': [
       {
         'id': 1,
         'name': 'John'
       }
     ]
  }))

## おまじない
if __name__ == "__main__":
    app.run(debug=True,threaded=True)
