import urllib2
from bs4 import BeautifulSoup
from flask import Flask, request, redirect
from twilio import twiml
import os
from time import strftime, localtime

app = Flask(__name__)

def Gore_Conditions():
    """
    Gets conditions for Gore Mountain including number of trails, number of
    lifts, new snow, and snow conditions
    """
    
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
    
    # format the response text
    response = "Ski report for Gore Mountain: \n" + trails + lifts  +'\n'+ depth +'\n'+ surface1 +'\n'+ surface2 +'\n'+ skiBowl +'\n'+ newSnow +'\n'+ makeSnow

    return response

def Get_Name(index, words):
    """
    Returns all the words as a single string that after index 
    without changing format. Should be name of a trail at Gore Mountain
    """
    i = index + 1
    name = ""
    while i < len(words):
        name += str(words[i])
        i += 1
        # add a space unless its the last word
        if i < len(words):
            name += " "
    return name
                     
def Trail_Search(trail_name):
    """
    Search for a trail and return the status
    none, none: trail not found
    -1, -1: closed (and not groomed)
    > 0, -1: open and not groomed
    > 0, > 0: open and groomed
    """
    page = urllib2.urlopen("http://www.goremountain.com/mountain/snow-report")
    soup = BeautifulSoup(page)
    
    try:
        results = soup.find(text= trail_name)
        open_trail  = results.findNext("span")
        groom_trail = open_trail.find_next()
    except:
        return None, None
    
    return str(open_trail).find("open"), str(groom_trail).find("groomed")


@app.route("/", methods=['GET', 'POST'])
def ski_report():
    
    try:
        # break incoming text into a list of words
        body = request.values.get("Body", None)
        text = body.split(' ')
    except:
        # for testing use
        body = "Gore mountain trail Half 'n' Half"
        text =  body.split(' ')

    # only supports Gore Mountain 
    if text[0].lower() == "gore":
        
        # if the word trail appears in the text, assume a lookup for a specific trail
        if "trail" in text:
            index = text.index("trail")
            # trail name is whatever comes after "trail"
            trail_name = Get_Name(index, text)
            o_stat, g_stat = Trail_Search(trail_name)

            if o_stat > 0:
                resp_body = trail_name + " is open"
                if g_stat > 0:
                    resp_body += " and groomed!"
                else:
                    resp_body += "!"
            else:
                if o_stat == None:
                    resp_body = "Sorry could not find trail: " + trail_name
                else:
                    resp_body = trail_name + " is closed :( "

        # respond with mountain conditions
        else:
            resp_body = Gore_Conditions()
    # first word was not "gore" so I don't know what to do!
    else:
        resp_body = "Sorry we do not currently support '" + text[0] + "'. Trying sending 'Gore' for realtime mountain updates."

#    resp_body += "\n\n" + strftime("%a, %d %b %Y %X", localtime())

    resp = twiml.Response()
    resp.message(resp_body)
    return str(resp)


@app.route("/voice/", methods=['GET', 'POST'])
def Welcome():
    # trying voice call out
    resp = twiml.Response()
    resp.say("Thank you for calling! You may also text this number to receive ski condition updates for Gore Mountain.")
    return str(resp)


if __name__ == "__main__":
    port = int(os.environ.get('PORT', 8000))
    app.run(host="0.0.0.0",port=port, debug=True)
