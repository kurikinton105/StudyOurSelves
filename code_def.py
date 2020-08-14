import datetime
import json
from difflib import SequenceMatcher
import numpy as np
from flask_bcrypt import Bcrypt
#時間の判定をしてまだのものを表示する。
def calender_sort(ToDoList_json): # ソートするjsonデータ（ToDo)
    sort_data = sorted(ToDoList_json, key=lambda x: x["date"]) #ここでソートする。
    today = datetime.date.today()
    showListIndex =[] #最後に表示するインデックス作成
    sort_cut_data =[] #ソートした後のデータ配列
    for i in range(len(sort_data)):
        limitdate = datetime.datetime.strptime(sort_data[i]["date"], '%Y-%m-%d')
        tdate = datetime.date(limitdate.year, limitdate.month, limitdate.day) #日付だけを取り出し
        if tdate >= (today):
            showListIndex.append(i)

    for i in range(len(showListIndex)):
        #print(sort_data[showListIndex[i]])
        sort_cut_data.append(sort_data[showListIndex[i]])
    return sort_cut_data

#サーチの機能
def search_class(search_text,classlist_json): #search_text:検索語,classlist_json class情報
    find_class_index =[]
    s_len = len(search_text)
    for i in range(len(classlist_json)):
        trg = classlist_json[i]['class']
        t_len = len(trg)
        r = max([SequenceMatcher(None, search_text, trg[i:i+s_len]).ratio() for i in range(t_len-s_len+1)])
        find_class_index.append(r) #類似度を入れ込む

    find_class_index_np = np.array(find_class_index) #Numpy配列に変換
    find_class_index_np_index=np.argsort(find_class_index_np)[::-1] #ソート後のインデックス
    result_class =[]
    #リストで表示
    if len(find_class_index_np_index) >= 10: #10個以上あった時は場合分け
        for i in range(10):
            result_class.append(classlist_json[find_class_index_np_index[i]])
    else:
        for i in range(len(find_class_index_np_index)):
            result_class.append(classlist_json[find_class_index_np_index[i]])
    return result_class

#ハッシュでのパスワード認証の実装
def hash_password(password_input,database_pass,bcrypt): #入力パスワード,でエータベースのハッシュ値
    #bcrypt = Bcrypt()
    if bcrypt.check_password_hash(database_pass,password_input) == 1:
        print("ハッシュによる認証ができました。")
    else:
        print("ハッシュによる認証に失敗")
    return bcrypt.check_password_hash(database_pass,password_input)
"""
bcrypt = Bcrypt()
password_data = bcrypt.generate_password_hash('password').decode('utf-8')
password ="password"
print(password_data)
password_hash = "$2b$12$Ry.bwY9XE3mcWHpMO3mgtu.Xq6MNuB/a3FkrqqfDg6Uyf87omE28W"
result = hash_password(password,password_hash,bcrypt)

print(result)
"""