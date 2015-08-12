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

#File to store the last tweet's id
file = "/twitterBot/max_id.txt"

#Function to ask Wolframalpha and return the answer
def wolfram_alpha(str):
        str=str.lower()
        str=str.replace("@berry_bots"," ")
        str=str.replace("."," ")
        str=str.replace("hi berry bots"," ")
        str=str.replace("hello berry bots"," ")
        str=str.replace("berry bots"," ")
        str=str.replace("berry bot"," ")
        str=str.strip()
        str=str.encode('utf-8')
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

#Reading file for last tweet's id
max=open(file,"r")
max.seek(0,0)
mid=max.read(18)

search_results = None

#Searching Twitter for Questions
try:
        search_results = twitter.search(q="@berry_bots",lang="en",count=5,since_id=str(mid))

except TwythonError as err:
        print err

max.close()

mxd = None

#Traversing the tweets searched and tweeting back the answers
try:
        if search_results:
                for tweet in reversed(search_results["statuses"]):
                        mxd = tweet["id_str"]
                        answer = wolfram_alpha(tweet["text"])
                        if answer!='x':
                                reply_id = tweet["id_str"]
                                reply_user = '@' + tweet['user']['screen_name']
                                reply_user = reply_user.encode('utf-8')
                                if len(answer)>123:
                                        n=123
                                        for i in range(0, len(answer), n):
                                                ans=answer[i:i+n]
                                                ans = reply_user + ' ' + ans
                                                twitter.update_status(status=ans,in_reply_to_status_id=reply_id)
                                                time.sleep(5)
                                else:
                                        answer = reply_user + ' ' + answer
                                        twitter.update_status(status=answer,in_reply_to_status_id=reply_id)
                                        time.sleep(5)


except TwythonError as e:
        print e

#Writing the id if the last replied tweet into the file
if mxd:
        max=open(file,"w")
        max.write(mxd)
        max.close()

