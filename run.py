import urllib2
from bs4 import BeautifulSoup
from flask import Flask, request, redirect
from twilio import twiml
import os
from time import strftime, localtime

app = Flask(__name__)

def Gore_Conditions():
    
    page = urllib2.urlopen("http://www.goremountain.com/mountain/snow-report")
    soup = BeautifulSoup(page)
    
    trails   = str(soup.find("div", "alpineTrailsLeft").get_text())
    lifts    = str(soup.find("div", "alpineLiftsLeft").get_text())
    depth    = soup.find("div", "alpineConditionsRightRow")
    surface1 = depth.find_next().find_next()
    surface2 = surface1.find_next().find_next()
    skiBowl  = surface2.find_next().find_next().find_next()
    newSnow  = skiBowl.find_next().find_next()
    makeSnow = newSnow.find_next().find_next()
    depth    = str(depth.get_text()) 
    surface1 = str(surface1.get_text()) 
    surface2 = str(surface2.get_text()) 
    skiBowl  = str(skiBowl.get_text())
    newSnow  = str(newSnow.get_text())
    makeSnow = str(makeSnow.get_text())
    
    response = "Ski report for Gore Mountain: \n" + trails + lifts  +'\n'+ depth +'\n'+ surface1 +'\n'+ surface2 +'\n'+ skiBowl +'\n'+ newSnow +'\n'+ makeSnow

    return response


@app.route("/", methods=['GET', 'POST'])
def ski_report():
    
    try:
        body = request.values.get("Body", None)
        text = body.lower().split(' ')
    except:
        body = "NONE "
        text =  body.lower().split(' ')

    if text[0] == "gore":
        resp_body = GoreConditions()
    else:
        resp_body = "Sorry we do not currently support '" + text[0] + "'. Trying sending 'Gore' for realtime mountain updates."

    resp_body += "\n\n" + strftime("%a, %d %b %Y %X", localtime())

    resp = twiml.Response()
    resp.message(resp_body)
    return str(resp)



if __name__ == "__main__":
    port = int(os.environ.get('PORT', 8000))
    app.run(host="0.0.0.0",port=port, debug=True)
