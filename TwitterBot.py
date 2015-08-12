#!/usr/bin/python

# Importing Twython
from twython import Twython

# Importing Wolfram
import urllib
import wolframalpha
import urllib2
from xml.etree import ElementTree as etree
import sys
import time

#Setting variables for Twitter
app_key = "*****YOUR APP KEY******"
app_secret = "****YOUR APP SECRET*****"
oauth_token = "*****YOUR OAUTH TOKEN******"
oauth_token_secret = "*****YOUR OAUTH TOKEN SECRET*****"

#Twython Object
twitter = Twython(app_key, app_secret, oauth_token, oauth_token_secret)

#Setting variables for Wolfram
app_id = "*****YOUR WOLFRAMALPHA APP ID******"

#Wolfram Object
client = wolframalpha.Client(app_id)

file = "/twitterBot/max_id.txt"

#Asking Wolfram
def wolfram_alpha(str):
        str=str.lower()
        str=str.replace("@berry_bots"," ")
        str=str.strip()
        res = client.query(str)
        if len(res.pods)>0:
                text=" "
                pod = res.pods[1]
                if pod.text:
                        text = pod.text.encode('utf-8')
                else:
                        text = 'x'
        else:
                text = 'x'
        return text;

#Searching Twitter for Questions
max=open(file,"r")
max.seek(0,0)
mid=max.read(18)
try:
        search_results = twitter.search(q="@berry_bots",lang="en",count=5,since_id=str(mid))
except TwythonError as e:
        print e
max.close()
mxd = None
for i in reversed(search_results["statuses"]):
        mxd=i["id_str"]
if mxd:
        max=open(file,"w")
        max.write(mxd)
        max.close()

try:
        for tweet in reversed(search_results["statuses"]):
                answer = wolfram_alpha(tweet["text"])
                if answer!='x':
                        reply_id = tweet["id_str"]
                        reply_user = '@' + tweet['user']['screen_name']
                        answer = reply_user + ' ' + answer
                        twitter.update_status(status=answer,in_reply_to_status_id=reply_id)
                        time.sleep(5)
except TwythonError as e:
        print e
