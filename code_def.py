import datetime
import json

#時間の判定をしてまだのものを表示する。
def calender_sort(ToDoList_json):
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

#ユーザーのクラス情報を取得する。
ToDoList = '[{"id": "class1","date":"2020-8-13","info":"期末課題"},{"id": "情報論理学","date":"2020-8-16","info":"猿でもわかる"},{"id": "機械学習","date":"2020-7-30","info":"未踏ジュニア"}]'
ToDoList_json = json.loads(ToDoList) #Json読み込み
print(calender_sort(ToDoList_json))
