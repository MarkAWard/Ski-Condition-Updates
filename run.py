from flask import Flask, request, redirect
from twilio import twiml
import os

app = Flask(__name__)

@app.route("/", methods=['GET', 'POST'])
def hello():
    resp = twiml.Response()
    resp.message("Hello, mobile monkey!")
    return str(resp)
#    return "Hello World!"


@app.route("/other")
def next():
    return "go away World!"

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 8000))
    app.run(host="0.0.0.0",port=port, debug=True)
