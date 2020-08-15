# SOS(Study_Ourselves)
## 概要
Study_Ourselvesは、暗記問題の共有＋締め切り共有を行うことができるWEBアプリケーションです。

2020/8/15,16に行われる[サマーハッカソン〜オンラインでLVupする夏合宿〜](https://tech-study-group.connpass.com/event/181146/)の参加作品です。

### 作成者
yama [@kurikinton105](https://github.com/kurikinton105)

tomSoya [@tomsoyaN](https://github.com/tomsoyaN)

jima884 [@jima884](https://github.com/jima884)

## 使うための前準備
#### ライブラリのインストール
1. コマンドでフォルダ内に移動し 
```bash
    $pip install -r requirements.txt
    または
    $py -m install -r requirements.txt
```
を実行する  

2.AzureなどのSQLサーバにて必要な情報を取得する。
詳しくはconfig.py内を参照

## デモ
#### AzureにWEBアプリケーションとして公開しています。



ローカル環境での実行方法

```bash
    export FLASK_APP=application.py
    flask run
```
#### WindowsのCMDプロンプトの場合
```bash
    set FLASK_APP=application.py
    flask run
```
#### Windowsのパワーシェルの場合
```bash
    $env:FLASK_APP = "application.py"
    flask run
```

127.0.0.1:5000にアクセスすることで,WEBアプリケーション版を利用できます.
