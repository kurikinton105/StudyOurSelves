from flask import Flask, render_template,request #追加
from flask import Flask
from flask import Flask,flash,redirect,render_template,request,session,abort
from api.views.user import user_router
from flask import Blueprint, request, make_response, jsonify
import json
app = Flask(__name__)

#Login処理の試しを作ってみる
app.secret_key = 'hogehoge'
# ------------------------------------------------------------------
@app.route('/')
def home():
   if not session.get('logged_in'):
       print("A")
       return render_template('login.html')
   else:
       str_out = ""
       str_out += "<h2>Congraturation!</h2>"
       str_out +=  "Hello<p />"
       str_out += "<a href='/logout'>Logout</a><br />"
#
       return str_out
# ------------------------------------------------------------------
@app.route('/login', methods=['POST'])
def do_admin_login():
   if request.form['username'] == 'test' \
       and request.form['password'] == 'password':
       session['logged_in'] = True
   else:
       flash('wrong password!')
   return home()
# ------------------------------------------------------------------
@app.route("/logout")
def logout():
   session['logged_in'] = False
   return home()

@app.route("/api")
def create_app():

  app.register_blueprint(user_router, url_prefix='/api')

  return app

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
