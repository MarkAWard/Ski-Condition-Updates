import urllib2
from bs4 import BeautifulSoup
from flask import Flask, request, redirect
from twilio import twiml
import os

app = Flask(__name__)

@app.route("/", methods=['GET', 'POST'])
def hello():
    
    message = str(request.values.get('body', None))

    page = urllib2.urlopen("http://www.goremountain.com/mountain/snow-report")
    soup = BeautifulSoup(page)
    trails  = str(soup.find("div", "alpineTrailsLeft").get_text())
    lifts   = str(soup.find("div", "alpineLiftsLeft").get_text())
    resp = twiml.Response()
    resp.message(message +" Ski report for Gore Mountain: \n" + trails + lifts)
    return str(resp)



if __name__ == "__main__":
    port = int(os.environ.get('PORT', 8000))
    app.run(host="0.0.0.0",port=port, debug=True)
