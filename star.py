import json
import os
import re
import urllib.request
from operator import eq
from bs4 import BeautifulSoup
from slackclient import SlackClient
from flask import Flask, request, make_response, render_template

app = Flask(__name__)

slack_token = "xoxp-506652758256-507380688323-507363497492-46c186f6b301793e17a363d1827d098a"
slack_client_id = "506652758256.507426597427"
slack_client_secret = "6d90131af74398728205cb27558533d9"
slack_verification = "dqw2lYyjTvgh7vgQpZnuvzRW"
sc = SlackClient(slack_token)

# 크롤링 함수 구현하기
def _crawl_naver_keywords(text):
    name_all=[] 
    keywords=[]
    list_all=[]
    list_href = []
    url = "http://www.fresh.com/KR/zodiac_2019.html"
    req = urllib.request.Request(url)

    sourcecode = urllib.request.urlopen(url).read()
    soup = BeautifulSoup(sourcecode, "html.parser")

    title_list = soup.find_all("div",class_="gallery")
    for i in range(int(len(title_list))):
        list_all.append(title_list[i].find("div").find("a")["href"])
    
    zodiac_name = soup.find_all("h6", class_="headline6")
    for j in zodiac_name:
        name_all.append(j.get_text())
    
    
    if name_all[1] in text:
        url = list_all[0]
        soup = BeautifulSoup(urllib.request.urlopen(url).read(), "html.parser")
        a = soup.find_all("p",class_="bodyCopy")
        b=[]
        for i in range(int(len(a))):
            b.append(a[i].get_text().strip())
        
        keywords=b[0:9]
    elif name_all[2] in text:
        url = list_all[1]
        soup = BeautifulSoup(urllib.request.urlopen(url).read(), "html.parser")
        a = soup.find_all("p",class_="bodyCopy")
        b=[]
        for i in range(int(len(a))):
            b.append(a[i].get_text().strip())
        
        keywords=b[0:10]
    elif name_all[3] in text:
        url = list_all[2]
        soup = BeautifulSoup(urllib.request.urlopen(url).read(), "html.parser")
        a = soup.find_all("p",class_="bodyCopy")
        b=[]
        for i in range(int(len(a))):
            b.append(a[i].get_text().strip())
        
        keywords=b[0:7]
    elif name_all[4] in text:
        url = list_all[3]
        soup = BeautifulSoup(urllib.request.urlopen(url).read(), "html.parser")
        a = soup.find_all("p",class_="bodyCopy")
        b=[]
        for i in range(int(len(a))):
            b.append(a[i].get_text().strip())
        
        keywords=b[0:7]
    elif name_all[5] in text:
        url = list_all[4]
        soup = BeautifulSoup(urllib.request.urlopen(url).read(), "html.parser")
        a = soup.find_all("p",class_="bodyCopy")
        b=[]
        for i in range(int(len(a))):
            b.append(a[i].get_text().strip())
        
        keywords=b[0:11]
    elif name_all[6] in text:
        url = list_all[5]
        soup = BeautifulSoup(urllib.request.urlopen(url).read(), "html.parser")
        a = soup.find_all("p",class_="bodyCopy")
        b=[]
        for i in range(int(len(a))):
            b.append(a[i].get_text().strip())
        
        keywords=b[0:11]
    elif name_all[7] in text:
        url = list_all[6]
        soup = BeautifulSoup(urllib.request.urlopen(url).read(), "html.parser")
        a = soup.find_all("p",class_="bodyCopy")
        b=[]
        for i in range(int(len(a))):
            b.append(a[i].get_text().strip())
        
        keywords=b[0:8]
    elif name_all[8] in text:
        url = list_all[7]
        soup = BeautifulSoup(urllib.request.urlopen(url).read(), "html.parser")
        a = soup.find_all("p",class_="bodyCopy")
        b=[]
        for i in range(int(len(a))):
            b.append(a[i].get_text().strip())
        
        keywords=b[0:10]
    elif name_all[9] in text:
        url = list_all[8]
        soup = BeautifulSoup(urllib.request.urlopen(url).read(), "html.parser")
        a = soup.find_all("p",class_="bodyCopy")
        b=[]
        for i in range(int(len(a))):
            b.append(a[i].get_text().strip())
        
        keywords=b[0:8]
    elif name_all[10] in text:
        url = list_all[9]
        soup = BeautifulSoup(urllib.request.urlopen(url).read(), "html.parser")
        a = soup.find_all("p",class_="bodyCopy")
        b=[]
        for i in range(int(len(a))):
            b.append(a[i].get_text().strip())
        
        keywords=b[0:9]
    elif name_all[11] in text:
        url = list_all[10]
        soup = BeautifulSoup(urllib.request.urlopen(url).read(), "html.parser")
        a = soup.find_all("p",class_="bodyCopy")
        b=[]
        for i in range(int(len(a))):
            b.append(a[i].get_text().strip())
        
        keywords=b[0:8]
    else:
        url = list_all[11]
        soup = BeautifulSoup(urllib.request.urlopen(url).read(), "html.parser")
        a = soup.find_all("p",class_="bodyCopy")
        b=[]
        for i in range(int(len(a))):
            b.append(a[i].get_text().strip())
        
        keywords=b[0:8]
    
    return u'\n'.join(keywords)

# 이벤트 핸들하는 함수
def _event_handler(event_type, slack_event):
    print(slack_event["event"])

    if event_type == "app_mention":
        channel = slack_event["event"]["channel"]
        text = slack_event["event"]["text"]

        keywords = _crawl_naver_keywords(text)
        sc.api_call(
            "chat.postMessage",
            channel=channel,
            text=keywords
        )

        return make_response("App mention message has been sent", 200,)

    # ============= Event Type Not Found! ============= #
    # If the event_type does not have a handler
    message = "You have not added an event handler for the %s" % event_type
    # Return a helpful error message
    return make_response(message, 200, {"X-Slack-No-Retry": 1})

@app.route("/listening", methods=["GET", "POST"])
def hears():
    slack_event = json.loads(request.data)

    if "challenge" in slack_event:
        return make_response(slack_event["challenge"], 200, {"content_type":
                                                             "application/json"
                                                            })

    if slack_verification != slack_event.get("token"):
        message = "Invalid Slack verification token: %s" % (slack_event["token"])
        make_response(message, 403, {"X-Slack-No-Retry": 1})
    
    if "event" in slack_event:
        event_type = slack_event["event"]["type"]
        return _event_handler(event_type, slack_event)

    # If our bot hears things that are not events we've subscribed to,
    # send a quirky but helpful error response
    return make_response("[NO EVENT IN SLACK REQUEST] These are not the droids\
                         you're looking for.", 404, {"X-Slack-No-Retry": 1})

@app.route("/", methods=["GET"])
def index():
    return "<h1>Server is ready.</h1>"

if __name__ == '__main__':
    app.run('0.0.0.0', port=8080)
