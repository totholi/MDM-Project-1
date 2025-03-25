from flask import Flask
from flask.helpers import send_file

app = Flask(__name__)

@app.route("/")
def initialPage():
    return send_file("index.html")

@app.route("/index")
def indexPage():
    return send_file("index.html")

@app.route("/result",methods=['POST'])
def resultPage():
    return send_file("result.html")