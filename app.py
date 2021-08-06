# -*- coding: utf-8 -*-
#load the modules required
import tweepy
import telepot, urllib3
import time
import json
from pprint import pprint
from telepot.loop import MessageLoop
from database import *

#load twitter and telegram secret and token authentication keys
with open('config.json', 'r') as data:
    apii = json.load(data)
#telegram api
auth = tweepy.OAuthHandler(
    apii['twitter']['api_key'],apii['twitter']['api_secret'])
auth.set_access_token(apii['access']['token'],apii['access']['secret'])
#twitter api
api = tweepy.API(auth)



proxy_url = 'http://proxy.server:3128'
telepot.api._pools = {
	'default': urllib3.ProxyManager(proxy_url=proxy_url, num_pools=3, maxsize=10,retries=False,timeout=30)
}

telepot.api._onetime_pool_spec = (urllib3.ProxyManager, dict(proxy_url=proxy_url,num_pools=1,maxsize=1,retries=False,timeout=30))
welcomeMessage = 'Hi, welcome to Twitter Trends.\n\
We will update you on latest trends on available locations of your choosing.\n\
/help to get manual'
manual = '@twi_trends - get latest trends on your set location.\n\
@twi_trends location - get trends of location of trends you provided.\n'
user = {"user_id": 0, "hour_update": 0, "min_update": 0, "location": ""}
questions = ['Which is your prefered location?(Ensure correct spelling!)',
'How often do you want to receive updates?(minimum-6min, maximum-23hrs)',
'Location not currently supported?You will recieve worldwide trends.']
bot = telepot.Bot(apii['bot']['token'])



def trends_in_string(trnds):
	"""
	function to string the trends in a vertically
	"""
	n = ''
	for i in range(len(trnds)):
		n =n + unicode((i+1))+'. ' +unicode(trnds[i].decode('utf8')) + '\n'
	return n

def get_tweets(location):
	"""
	returns the trending topics from the location provided
	"""
	try:

		trend_place = api.trends_place(get_woeid(location)[0])[0]
		trends = trend_place['trends']
		num_of_trends = len(trends)
		l = []
		for i in range(num_of_trends):
			l.append(trends[i]['name'])
		return trends_in_string(l)
	except:
		return 'No tweets Found!'

def handle(msg):
	"""
	message handler, text typed in telegram chat
	"""
	content_type, chat_type, chat_id = telepot.glance(msg)
	print content_type, chat_type, chat_id
	if content_type == 'text':
		if msg['text'] == '/start' and user_info(chat_id) is None:
			insert(chat_id)
			bot.sendMessage(chat_id, welcomeMessage)
		if msg['text'] == '/help':
			bot.sendMessage(chat_id, manual)
		if msg['text'].startswith('/location'):
			loc = msg['text'].split(' ')
			if len(loc) == 1:
				bot.sendMessage('You have not provided the location!')
			else:
				update_info(chat_id,**{'location':loc[1]})
		if msg['text'].startswith('/time'):
			loc = msg['text'].split(' ')
			if len(loc) == 1:
				bot.sendMessage('You have not provided the time!')
			else:
				update_info(chat_id,**{'mupdate':loc[1]})
		if msg['text'] == '/trends':
			bot.sendMessage(chat_id, get_tweets(user_info(chat_id)[0][2]))
 

if __name__ == '__main__':
	MessageLoop(bot, handle).run_as_thread()
	print 'Listening ...'
	while 1:
		time.sleep(5)
