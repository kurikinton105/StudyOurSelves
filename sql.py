
import pyodbc
from config import server,database,username,password,driver #パスワードの入れ込み
import datetime
#--------------------insert系-----------------------------
def insert_user(ID,email,password_user): #ユーザーのインサートを行う、Username,Mail,Pass
    with pyodbc.connect('DRIVER='+driver+';SERVER='+server+';PORT=1433;DATABASE='+database+';UID='+username+';PWD='+ password) as conn:
        with conn.cursor() as cursor:
            sql = "INSERT INTO [dbo].[UserInfo] (UserName,Mail,Pass) VALUES(N'"+ID+"', '"+email + "','" +password_user +"');"
            cursor.execute(sql)
            conn.commit()
            print("ユーザーの登録が終わりました")

def make_class(class_name,class_info): #クラス情報のインサート
    with pyodbc.connect('DRIVER='+driver+';SERVER='+server+';PORT=1433;DATABASE='+database+';UID='+username+';PWD='+ password) as conn:
        with conn.cursor() as cursor:
            sql = "INSERT INTO [dbo].[ClassInfo] (ClassName,Info) VALUES(N'" + class_name + "' , N'"+class_info+"');" #日本語にはNをつける
            print(sql)
            cursor.execute(sql)
            conn.commit()
            print("クラスの登録が終わりました")

def Taking_class(UserId2,classid): #クラス情報のインサート(ここはid番号で処理を行う。)授業登録で使う。
    with pyodbc.connect('DRIVER='+driver+';SERVER='+server+';PORT=1433;DATABASE='+database+';UID='+username+';PWD='+ password) as conn:
        with conn.cursor() as cursor:
            sql = "INSERT INTO [dbo].[TakingClasses] (UserId,ClassId) VALUES('" + str(UserId2) + "' , '"+str(classid)+"');" #日本語にはNWOつける
            cursor.execute(sql)
            conn.commit()
            print("クラスの登録が終わりました")

def ToDo_insert(ClassId,TodoName,TodoDate,TodoInfo): #ToDO情報のインサート
    with pyodbc.connect('DRIVER='+driver+';SERVER='+server+';PORT=1433;DATABASE='+database+';UID='+username+';PWD='+ password) as conn:
        with conn.cursor() as cursor:
            sql = "INSERT INTO [dbo].[Todos] (ClassId,TodoName,TodoDate,TodoInfo) VALUES('" + str(ClassId) + "' , N'"+TodoName+ "' , N'"+(TodoDate)+ "' , N'"+TodoInfo+"');" #日本語にはNWOつける
            cursor.execute(sql)
            conn.commit()
            print("クラスの登録が終わりました")

# ----------------------get系-----------------------------
def getpassword(user_id): #パスワードの取得 user_id return
    with pyodbc.connect('DRIVER='+driver+';SERVER='+server+';PORT=1433;DATABASE='+database+';UID='+username+';PWD='+ password) as conn:
        with conn.cursor() as cursor:
            sql = "SELECT * FROM UserInfo WHERE UserName = '"+user_id+"';"
            cursor.execute(sql)
            rows = cursor.fetchall()
            print("ユーザ情報",rows[0][0],rows[0][1],rows[0][2],rows[0][3])
            print("ユーザーの検索が終わりました")
            return rows[0][0],rows[0][1],rows[0][2],rows[0][3]
def getuserlist(): #ユーザ情報だけ
    with pyodbc.connect('DRIVER='+driver+';SERVER='+server+';PORT=1433;DATABASE='+database+';UID='+username+';PWD='+ password) as conn:
        with conn.cursor() as cursor:
            sql = "SELECT UserName FROM UserInfo ;"
            cursor.execute(sql)
            rows = cursor.fetchall()
            print("ユーザ情報",rows)
            user_list =[]
            for i in range(len(rows)):
                user_list.append(rows[i][0])
            print("ユーザーの検索が終わりました")

            return user_list

def get_classinfo(class_name): # クラス情報を取得する(クラスネーム)：出力
    with pyodbc.connect('DRIVER='+driver+';SERVER='+server+';PORT=1433;DATABASE='+database+';UID='+username+';PWD='+ password) as conn:
        with conn.cursor() as cursor:
            sql = "SELECT Info FROM UserInfo WHERE UserName = '"+class_name+"';"
            cursor.execute(sql)
            rows = cursor.fetchall()
            #rows=rows.encode("utf8")
            print("ユーザ情報",rows)
            print("クラス情報の検索が終わりました")
            return rows[0][0]

def get_class_all(): # クラスの全ての情報を取得する(クラスネーム)：出力
    with pyodbc.connect('DRIVER='+driver+';SERVER='+server+';PORT=1433;DATABASE='+database+';UID='+username+';PWD='+ password) as conn:
        with conn.cursor() as cursor:
            sql = "SELECT * FROM [dbo].[ClassInfo];"
            cursor.execute(sql)
            rows = cursor.fetchall()
            #rows=rows.encode("utf8")
            print("ユーザ情報",rows)
            print("クラス情報の検索が終わりました")
            #class_name_from_index = get_classname_from_index(rows[0][0])
            #print(class_name_from_index)
            return rows[0][0]

def get_Taking_class(UserIndex):# TakingClassesユーザが取っているクラスの取得
    with pyodbc.connect('DRIVER='+driver+';SERVER='+server+';PORT=1433;DATABASE='+database+';UID='+username+';PWD='+ password) as conn:
        with conn.cursor() as cursor:
            sql = "SELECT ClassId FROM [dbo].[TakingClasses] WHERE UserId = '"+str(UserIndex)+"';"
            cursor.execute(sql)
            rows = cursor.fetchall()
            #print("クラス情報",rows)
            print("取っているクラスの検索が終わりました")
            class_list_index = []
            for i in range(len(rows)):
                #print(rows[i][0])
                class_list_index.append(rows[i][0]) #クラス番号を追加
            #print(class_list_index)
            return class_list_index #取っているクラス番号の一覧を出力

def GetTodo(ClassId_list): #ユーザが取っているクラスのToDを返却します。（index,return:ToDoの情報）
    with pyodbc.connect('DRIVER='+driver+';SERVER='+server+';PORT=1433;DATABASE='+database+';UID='+username+';PWD='+ password) as conn:
        conn.setencoding('utf-8')
        with conn.cursor() as cursor:
            ToDoList_user =[]
            for i in range(len(ClassId_list)):
                sql = "SELECT * FROM [dbo].[ToDos] WHERE ClassId = '"+str(ClassId_list[i])+"';"
                cursor.execute(sql)
                rows = cursor.fetchall()
                #rows=rows.encode("utf8")
                print("クラスToDo情報",rows)
                if rows != []:
                    for i in range(len(rows)):
                        ToDoList_user.append(rows[i])
                #print("クラスのToDoの検索が終わりました")
            return ToDoList_user

def get_classname_from_index(class_index):#クラスidからクラスの名前を取得します。
    with pyodbc.connect('DRIVER='+driver+';SERVER='+server+';PORT=1433;DATABASE='+database+';UID='+username+';PWD='+ password) as conn:
        with conn.cursor() as cursor:
            sql = "SELECT ClassName FROM [dbo].[ClassInfo] WHERE ClassId = '"+str(class_index)+"';"
            cursor.execute(sql)
            rows = cursor.fetchall()
            print(rows[0][0])
            return rows[0][0]

#---------------ここからは実行するやつ-----------------------

#insert_user("example@co.jp","example@.co.jp","$2b$12$q.n/uI24z9zStg8tritvU.u4Vn6UkYkHDxwpz8Xt3OvMajIuvSBKi")
#Taking_class(1,1)
#make_class("情報論理学","お猿")
#ToDo_insert(2,"期末課題","2020-8-17","機械学習を利用したビジネス案を提案しまとめよ")




#-----------------------------------------------------------------
class COS5SQL:
    conn = None
    cursor = None

    def __enter__(self):
        self.conn = pyodbc.connect('DRIVER='+driver+';SERVER='+server+';PORT=1433;DATABASE='+database+';UID='+username+';PWD='+ password)
        self.cursor = self.conn.cursor()
        return self
    def __exit__(self, exc_type, exc_value, traceback):
        self.cursor.close()
        self.conn.close()
    
    def GetUserId(self,username):
        self.cursor.execute("SELECT UserId FROM [dbo].[UserInfo] WHERE UserName = '" + username + "'")
        row = self.cursor.fetchall()
        if(len(row) == 1):
            return row[0][0]
        elif(len(row) == 0):
            return None
        else:
            print("データベースエラー:複数Id存在")
    def GetClassId(self,classname):
        self.cursor.execute("SELECT ClassId FROM [dbo].[ClassInfo] WHERE ClassName = N'" + classname + "'")
        row = self.cursor.fetchall()
        if(len(row) == 1):
            return row[0][0]
        elif(len(row) == 0):
            return None
        else:
            print("データベースエラー:複数Id存在")

    def GetProblemSetInfo(self,classId):
        self.cursor.execute("SELECT * FROM [dbo].[ProblemSetInfo] WHERE ProblemSetId = (SELECT ProblemSetId FROM [dbo].[ClassProblemSets] WHERE ClassId=" + str(classId) +")" )
        rows = self.cursor.fetchall()
        return rows

    def GetProblemSet(self,setId):
        self.cursor.execute("SELECT * FROM [dbo].[Problem] WHERE ProblemId IN (SELECT ProblemId FROM [dbo].[ProblemSet] WHERE ProblemSetId=" + str(setId) +")" )
        rows = self.cursor.fetchall()
        return rows

    def InsertProblem(self,classId,setId,name,question,selections,answer):
        sql = "INSERT INTO [dbo].[Problem] (ClassId,ProblemName,ProblemText,Selection1,Selection2,Selection3,Selection4,Answer)\
              VALUES("+str(classId)+", N'"+ name + "',N'" +question + "',\
                  N'" +selections[0] + "',N'" +selections[1] + "',N'" +selections[2] + "',N'" +selections[3] + "'," +answer + ")"
        print(sql)
        self.cursor.execute(sql)
        self.conn.commit()
        self.cursor.execute("SELECT IDENT_CURRENT('dbo.Problem')")
        problemId = self.cursor.fetchone()[0]
        return problemId

    def AddProblem2Set(self,setId,problemId):
        self.cursor.execute("INSERT INTO [dbo].[ProblemSet] (ProblemSetId,ProblemId)  VALUES("+str(setId)+", " + str(problemId) + ")" )
        self.conn.commit()

    def RemoveClassFUser(self,userId,classId):
        self.cursor.execute("DELETE FROM [dbo].[TakingClasses] WHERE UserId = "+str(userId)+"AND ClassId =" + str(classId))
        self.conn.commit()

    def IsTakeClass(self,userId,classId):
        self.cursor.execute("SELECT * FROM [dbo].[TakingClasses] WHERE UserId = "+str(userId)+"AND ClassId =" + str(classId))
        rows = self.cursor.fetchone()
        print("-------------------------\n",rows)
        if(rows == None):
            return False
        else:
            return True

    def GetAllClasses(self):
        self.cursor.execute("SELECT * FROM [dbo].[ClassInfo]")
        rows = self.cursor.fetchall()
        return rows
        #--------------------insert系-----------------------------
    def insert_user(ID,email,password_user): #ユーザーのインサートを行う、Username,Mail,Pass
        with pyodbc.connect('DRIVER='+driver+';SERVER='+server+';PORT=1433;DATABASE='+database+';UID='+username+';PWD='+ password) as conn:
            with conn.cursor() as cursor:
                sql = "INSERT INTO [dbo].[UserInfo] (UserName,Mail,Pass) VALUES(N'"+ID+"', '"+email + "','" +password_user +"');"
                cursor.execute(sql)
                conn.commit()
                print("ユーザーの登録が終わりました")

    def make_class(class_name,class_info): #クラス情報のインサート
        with pyodbc.connect('DRIVER='+driver+';SERVER='+server+';PORT=1433;DATABASE='+database+';UID='+username+';PWD='+ password) as conn:
            with conn.cursor() as cursor:
                sql = "INSERT INTO [dbo].[ClassInfo] (ClassName,Info) VALUES(N'" + class_name + "' , N'"+class_info+"');" #日本語にはNWOつける
                cursor.execute(sql)
                conn.commit()
                print("クラスの登録が終わりました")

    def AddClass2User(self,userId,classId): #クラス情報のインサート(ここはid番号で処理を行う。)授業登録で使う。
                sql = "INSERT INTO [dbo].[TakingClasses] (UserId,ClassId) VALUES(" + str(userId) + " , " + str(classId) + ");" #日本語にはNWOつける
                self.cursor.execute(sql)
                self.conn.commit()
                print("クラスの登録が終わりました")

    def ToDo_insert(ClassId,TodoName,TodoDate,TodoInfo): #ToDO情報のインサート
        with pyodbc.connect('DRIVER='+driver+';SERVER='+server+';PORT=1433;DATABASE='+database+';UID='+username+';PWD='+ password) as conn:
            with conn.cursor() as cursor:
                sql = "INSERT INTO [dbo].[Todos] (ClassId,TodoName,TodoDate,TodoInfo) VALUES('" + str(ClassId) + "' , N'"+TodoName+ "' , N'"+TodoDate+ "' , N'"+TodoInfo+"');" #日本語にはNWOつける
                cursor.execute(sql)
                conn.commit()
                print("クラスの登録が終わりました")

    # ----------------------get系-----------------------------
    def getpassword(user_id): #パスワードの取得 user_id return
        with pyodbc.connect('DRIVER='+driver+';SERVER='+server+';PORT=1433;DATABASE='+database+';UID='+username+';PWD='+ password) as conn:
            with conn.cursor() as cursor:
                sql = "SELECT * FROM UserInfo WHERE UserName = '"+user_id+"';"
                cursor.execute(sql)
                rows = cursor.fetchall()
                print("ユーザ情報",rows[0][0],rows[0][1],rows[0][2],rows[0][3])
                print("ユーザーの検索が終わりました")
                return rows[0][0],rows[0][1],rows[0][2],rows[0][3]

    def get_classinfo(class_name): # クラス情報を取得する(クラスネーム)：出力
        with pyodbc.connect('DRIVER='+driver+';SERVER='+server+';PORT=1433;DATABASE='+database+';UID='+username+';PWD='+ password) as conn:
            with conn.cursor() as cursor:
                sql = "SELECT Info FROM UserInfo WHERE UserName = '"+class_name+"';"
                cursor.execute(sql)
                rows = cursor.fetchall()
                print("ユーザ情報",rows)
                print("クラス情報の検索が終わりました")
                return rows[0][0]

    def TakingClasses(user_id):# TakingClassesユーザが取っているクラスの取得
        with pyodbc.connect('DRIVER='+driver+';SERVER='+server+';PORT=1433;DATABASE='+database+';UID='+username+';PWD='+ password) as conn:
            with conn.cursor() as cursor:
                sql = "SELECT Pass FROM UserInfo WHERE UserName = '"+user_id+"';"
                cursor.execute(sql)
                rows = cursor.fetchall()
                print("ユーザ情報",rows[0][0])
                print("ユーザーの検索が終わりました")
                return rows[0][0]

    def get_Taking_class(UserIndex):
        with pyodbc.connect('DRIVER='+driver+';SERVER='+server+';PORT=1433;DATABASE='+database+';UID='+username+';PWD='+ password) as conn:
            with conn.cursor() as cursor:
                sql = "SELECT * FROM [dbo].[TakingClasses] WHERE UserId = '"+str(UserIndex)+"';"
                cursor.execute(sql)
                rows = cursor.fetchall()
                print("クラス情報",rows)
                print("取っているクラスの検索が終わりました")


                return rows[0][0]

#-------デバック
"""
print(getpassword("example@com3"))
print(get_class_all())
from code_def import search_class
with COS5SQL() as cos5sql:
    classlist = cos5sql.GetAllClasses()
    print(classlist)
    print(search_class("機会",classlist))
"""

#make_class("サマーハッカソン","2020年夏にアウトプットするぞ！！") #ここで作る。
#get_class_all()
#ToDo_insert(1,"中間課題","2020/8/14","8月15日までにやること")
#print(GetTodo([1]))
#Taking_class(0,1)

