from flask import Flask, render_template,request #追加
from flask import Flask
from flask import Flask,flash,redirect,render_template,request,session,abort
import flask ,flask_login
from api.views.user import user_router
from flask import Blueprint, request, make_response, jsonify
import json
import datetime
from api.__init__ import api_app
from code_def import calender_sort,search_class

app = Flask(__name__)

#Login処理の試しを作ってみる
app.secret_key = 'hogehoge'

class User(flask_login.UserMixin):
    pass

login_manager = flask_login.LoginManager()
login_manager.init_app(app)

#SQL実装前の仮データベース
users = {'example@com': {'password': 'password'}} #パスワード
classlist_user = ['class1','機械学習','情報論理学'] #本当はusersの中にSQLで格納してほしい
ToDoList = '[{"id": "class1","date":"2020-8-13","info":"期末課題"},{"id": "情報論理学","date":"2020-8-16","info":"猿でもわかる"},{"id": "情報論理学","date":"2020-8-16","info":"猿でもわかるっていうけど誰がわかるねんって感じでめっちゃ怒っているなうなので、なんとかしてほしい。"},{"id": "機械学習","date":"2020-7-30","info":"未踏ジュニア"}]'
ToDoList_json = json.loads(ToDoList) #Json読み込み
classlist = '[{"class": "class1","info":"期末課題"},{"class": "情報論理学","info":"猿でもわかる"},{"class": "機械学習","info":"猿でもわかる"}]'
classlist_json = json.loads(classlist) #Json読み込み

#----ここからページへのリンクの実装---------
error_flag = False
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
       print("最初のログイン")
       error_flag = False
       return render_template('index.html')
   else:
       print("ログインなう")
       #予定データのソート
       sort_cut_data = calender_sort(ToDoList_json) # ソートはcode_def.py内にて定義

       return render_template('home_ver2.html',id_name=flask_login.current_user.id, ToDo = sort_cut_data,classlist_user = classlist_user)


# ------------------------------------------------------------------
@app.route('/login')
def showloginpage():
    if error_flag == True:
        message = "ユーザー名がすでに使われているかパスワードが違います"
    else:
        message = ""
    return render_template('login_ver2.html',error_message = message)

@app.route('/new')
def newuserpage():
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
        error_flag = False
        #return home()
        return flask.redirect(flask.url_for('home'))
    else:
        flash('パスワードまたは、ユーザー名が違います。')

        return showloginpage()

@app.route('/protected')
@flask_login.login_required #ログインが必要だよ
def protected():
    print(flask_login.current_user.id)
    return render_template('home_ver2.html',id_name=flask_login.current_user.id)
    #return 'Logged in as: ' + flask_login.current_user.id

# -----個々のページの処理コード-----------------------------------------
# 授業検索のページ
@app.route('/register_class')
def register_class():
    return render_template('register_class.html',classlist = classlist_json)

#サーチの時の機能を追加
@app.route('/searchtext', methods=['POST']) #ここでログインのPOSTを行う
def searching():
    search_text = flask.request.form['searching'] #searchボックスの中身を取得
    print(search_text)
    search_json = search_class(search_text,classlist_json) #code_def内の関数でサーチ機能を実装
    #search_json2 = json.loads(search_json)
    return render_template('register_class.html',classlist = search_json)


# classページの動的作成
@app.route('/class/<classname>')
@flask_login.login_required
def classpage(classname):
    #データベースからclassnameを検索
    for i in range(len(classlist_json)):
        if classlist_json[i]['class'] == classname:
            info_class = classlist_json[i]['info']

    return render_template("class.html",classname = classname,info_class=info_class)

# edit
@app.route('/edit')
def edit_user():

    return render_template("class.html")

@app.route('/edit/passwordchange', methods=['POST']) #ここで、データベースの変更のポストを送る
def edit_userpassword():
    try:
        print("ここでデータベース操作")
        flash("パスワードの変更が完了しました。")
        return render_template("home.html")
    except:
        flash("エラーが発生しました。もう一度やり直してくだいさい")
        return render_template("class.html")



# 予定追加




#question




# ------------------------------------------------------------------
@app.route("/logout")
def logout():
   session['logged_in'] = False
   flask_login.logout_user()
   return home()


# ------------------------------------------------------------------
@app.route('/api', methods=['GET'])
@flask_login.login_required
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
