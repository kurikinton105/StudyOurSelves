from flask import Flask, render_template,request #追加
from bag_of_words import bag_of_words_sum
from MakeClassEasy import MakeClassEasy
from flask import Flask
from flask import Flask,flash,redirect,render_template,request,session,abort

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




@app.route("/make", methods=["GET", "POST"])
def main_page():
    if request.method == 'GET':
        #print("GET")
        text = "ここに結果が出力されます"
        data_word = [" "]
        val = False
        return render_template("make-class-easy.html",text=text,data_word=data_word,val = val)
    elif request.method == 'POST':
        #print("POST")
        val = True #フラグを１にする
        text = request.form["input_text"]
        try:
            result,data_word = bag_of_words_sum(str(text),50,100)
            return render_template("make-class-easy.html",text=result,data_word=data_word,val = val)
        except:
            return render_template("make-class-easy.html",text="Error:文章は２文以上にしてください。もう一度文章を入力してください")


@app.route("/develop", methods=["GET", "POST"])
def develop_page():
    if request.method == 'GET':
        #print("GET")
        text = "ここに結果が出力されます"
        data_word = [" "]
        val = False
        return render_template("make-class-easy-develop.html",text=text,data_explain=data_word,val = val)
    elif request.method == 'POST':
        #print("POST")
        val = True #フラグを１にする
        text = request.form["input_text"]
        try:
            if(request.args.get('c') == None):
                c= 3
            else:
                c = int(request.args.get('c'))
        except:
            return render_template("make-class-easy-develop.html",text="Error:不正なクエリパラメータ。使い方:URLの最後に?c=数値　をつけてください。")
        try:
            result,explains,time = MakeClassEasy(str(text),50,100,c)
            return render_template("make-class-easy-develop.html",text=result,data_explain=explains,val = val,process_time = time)
        except:
            return render_template("make-class-easy-develop.html",text="Error:文章は２文以上にしてください。もう一度文章を入力してください")


## おまじない
if __name__ == "__main__":
    app.run(debug=True,threaded=True)
