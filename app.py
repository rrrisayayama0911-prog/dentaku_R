# _*_ coding: utf-8 _*_
from builtins import FileNotFoundError

from flask import Flask, request,render_template, redirect, \
    url_for  # request：受け取ったデータの取得。render_template:HTMLテンプレートファイルを動的に生成し、ユーザーに返す役割を担う
import re
import chromedriver_autoinstaller
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import os
import requests
from bs4 import BeautifulSoup

# グローバルで定義
cashed_data = None

# ChromeDriverの自動インストール（Chromeのバージョンに対応したものをDL）
chromedriver_autoinstaller.install()

# Chrome本体のパス
chrome_binary_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
print("Chrome本体:", os.path.isfile(chrome_binary_path))

# Chromeがなければ終了
if not os.path.isfile(chrome_binary_path):
    raise FileNotFoundError("Chrome.exe が見つかりません: {chrome_binary_path}")

# オプション設定
options = Options()
options.binary_location = chrome_binary_path

"""
Flask = キッチンのシェフ（Pythonで軽量なWebアプリケーションを構築するためのマイクロフレームワーク）
HTML = お皿
CSS = 盛り付け
JavaScript = お客さんが料理を選んだ時のアクション（注文ボタンとか）
"""

# 基本的なアプリはインスタンスを作成,Flask(...) は Flask クラスの呼び出し
app = Flask(__name__)

# キャッシュ変数を定義(最初はNone)
cached_data = None
history = []  # 計算履歴を保存するリスト


# Webアプリ（HTML返す）
@app.route("/", methods=["GET", "POST"])
def index():
    global history
    global cashed_data
    result = None

    if request.method == "POST":
        expression = request.form.get("expression")
        if expression:
            expression = expression.translate(str.maketrans(
                "０１２３４５６７８９＋－＊／％（）",
                "0123456789+-*/%()"
            )).replace("　", "")
        expression = re.sub(r"(\d)(\()", r"\1*\2", expression)
        expression = re.sub(r"(\))(\d)", r"\1*\2", expression)
        try:
            result_value = eval(expression)
            result = f"{result_value}"
            history.append({"expression": f"{expression}={result_value}"})
        except Exception:
            result = "文字（例: あ、Aなど）は使えません。"

    print("リクエストメソッド:", request.method)
    print("フォームの中身！！:", request.form)
    print("今までの履歴の中身:", history)

    return render_template("index.html", result=result, history=history)


@app.route("/memo", methods=["POST"])
def save_memo():
    index = int(request.form["index"])
    memo_value = request.form["memo_value"]
    if 0 <= index < len(history):
        history[index]["memo"] = memo_value
        return redirect("/")





# 個別削除
@app.route("/delete_one/<int:index>", methods=["POST"])  # URLの一部として引数を渡す場合は、ルートに / が必要
def delete_one(index):
    if 0 <= index < len(history):
        del history[index]
    return redirect("/")


# 全削除
@app.route("/delete", methods=["post"])
def delete():
    history.clear()
    return redirect("/")



@app.route("/scrape")
def scrape_google():
    driver = webdriver.Chrome(options=options)
    driver.get("https://www.google.com")
    # ここで適切な要素を取得する
    return "ページアクセス完了"

@app.route("/page1",methods=["GET"])
def page1():
    return render_template("page1.html")

#「/page2」へアクセスがあった場合に、page2.htmlを返す
@app.route("/page2",methods=["GET"])
def page2():
    return render_template("page2.html")

@app.route("/page3",methods=["GET"])
def page3():
    return render_template("page3.html")

@app.route("/menu") #リンク一覧ページ
def menu():
    return render_template("menu.html")

#app.pyをターミナルから直接呼び出した時だけ、app.run()を実行する
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)  # run() は Flask インスタンス app の メソッド、app.run()でサーバーを起動
