from flask import Flask, render_template,request #追加
from flask import Flask
from flask import Flask,flash,redirect,render_template,request,session,abort
import flask ,flask_login
from api.views.user import user_router
from flask import Blueprint, request, make_response, jsonify
import json
import datetime
from api.__init__ import api_app
from code_def import calender_sort

app = Flask(__name__)

#Login処理の試しを作ってみる
app.secret_key = 'hogehoge'

class User(flask_login.UserMixin):
    pass

login_manager = flask_login.LoginManager()
login_manager.init_app(app)

#SQL実装前の仮データベース
users = {'example@com': {'password': 'password'}}
ToDoList = '[{"id": "class1","date":"2020-8-13","info":"期末課題"},{"id": "情報論理学","date":"2020-8-16","info":"猿でもわかる"},{"id": "情報論理学","date":"2020-8-16","info":"猿でもわかるっていうけど誰がわかるねんって感じでめっちゃ怒っている"},{"id": "機械学習","date":"2020-7-30","info":"未踏ジュニア"}]'
ToDoList_json = json.loads(ToDoList) #Json読み込み

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
    email = request.form.get('email')
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
       #予定データのソート
       sort_cut_data = calender_sort(ToDoList_json)

       return render_template('home_ver2.html',id_name=flask_login.current_user.id, ToDo = sort_cut_data)
# ------------------------------------------------------------------
@app.route('/login')
def showloginpage():
    return render_template('login_ver2.html')

@app.route('/new')
def newuserpage():
    error_flag = False
    if error_flag == True:
        message = "ユーザー名がすでに使われているかパスワードが違います"
    else:
        message = ""
    return render_template('new.html',error_message = message)
#database

@app.route('/loginpost', methods=['POST']) #ここでログインのPOSTを行う
def do_admin_login():
    id_name = flask.request.form['email'] #ユーザーネームの取り出し
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
    return render_template('home_ver2.html',id_name=flask_login.current_user.id)
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
