class SystemConfig:

  DEBUG = True

  SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://{user}:{password}@{host}/{db_name}?charset=utf8'.format(**{
      'user': '<接続ユーザー>',
      'password': '<接続パスワード>',
      'host': '<接続先ホスト>',
      'db_name': '<接続先データベース名>'
  })

Config = SystemConfig