from __future__ import absolute_import, unicode_literals
from celery import shared_task
from celery.utils.log import get_task_logger
import json
import os
import oauth2 as oauth
from .models import Tweet, myTweet
from django.utils import timezone
import urllib
import urllib2
import re
from .summarizer import summarize


print('Task file')
logger=get_task_logger(__name__)

consumer_key =  'klmNdnzEXXuDmO5fkBHGf7a2B' #os.environ.get('CONSUMER_KEY')
consumer_secret = 'HsYcgxpcdwKchwalGB3GBKDb2IjGNFV4JpKRzdLV7BR6n9XbBJ'#os.environ.get('CONSUMER_SECRET')
access_token = '908328492428922880-ilZsDGwXiEdoWvHEhhRIqsuD7LHS79t'#os.environ.get('ACCESS_TOKEN')
access_token_secret = 'qd6idimdpWpoOiElgD1BuMdqGX08HLUEC58JgussJvYao' #os.environ.get('ACCESS_TOKEN_SECRET')

consumer = oauth.Consumer(key=consumer_key,secret=consumer_secret)
access_token = oauth.Token(key=access_token,secret=access_token_secret)
client = oauth.Client(consumer,access_token)


	

@shared_task
def getTweets():
	trendsUrl = 'https://api.twitter.com/1.1/trends/place.json?id=23424977'
	embedUrl = 'https://publish.twitter.com/oembed?url=https%3A%2F%2Ftwitter.com%2FInterior%2Fstatus%2F'#EmbededURL for aa vise tweeten paa siden
	resopnse, data = client.request(trendsUrl) #Faar tak trender i USA
	trends = json.loads(data)
	trends2 = []
	for i in range(0,5):#Plukker ut 5 trender og bytter # med %23 for at det skal gaa i URLen
		trends2.append(trends[0]['trends'][i]['name'].replace('#','%23'))
	getTweetsUrl = 'https://api.twitter.com/1.1/search/tweets.json?q=%s+since:2017-09-07&count=5&result_type=popular&tweet_mode=extended'
	textSum = ''
	Tweet.objects.all().delete()
	for trend in trends2:# Faar tak i tweeter for de fem overste trendene
		response, data = client.request((getTweetsUrl%trend).encode('ascii'))
		tweets = json.loads(data)
		if tweets['statuses']:#Dytter tweetene i databasen og tar vare paa tekst
			for tweet in tweets['statuses']:
				req = urllib2.Request(embedUrl+tweet['id_str'])
				resp = urllib2.urlopen(req)
				html = json.load(resp)['html']
				Tweet.objects.create(tweet_id=tweet['id_str'],text=tweet['full_text'],publish_date=timezone.now().date(),html=html)				
				textSum += ' ' + tweet['full_text']
	logger.info('Got Tweets')
	#tar aa rensker tweeten
	#tekst1 = re.sub(r'[\U0001f000-\U0001ffff]',' ',textSum)# fjerner emoji. Tror ikke den fjerner alle emojiene
	tekst2 = re.sub(r'[\n]{1}',' ',textSum)#Fjerner \n
	tekst22 = re.sub(r'(&amp;)','&',tekst2)#bytter &amp; med &
	tekst3 = re.sub(r'([(https){1}(http){1}]{4,5}:\/\/){1}[^\.]+[.]{1}[\w]{2,3}[\S]+',' ',tekst22)#Fjerner nettadresser
	tekst4 = re.sub(r'[\s]+',' ',tekst3)# Gj0r mellomrom til et.
	tekstSum = summarize(tekst4,3)
	tekstSum2 = ''
	for tekst in tekstSum:
		tekstSum2 += ' ' + tekst
	tekstSum2.encode()
	postURL = 'https://api.twitter.com/1.1/statuses/update.json?' + urllib.urlencode({'status': tekstSum2.encode(errors='xmlcharrefreplace')})
	print(client.request(postURL,'POST'))


#regexp
# [\U0001f000-\U0001ffff] = bilder av typen \U0001f1fa
# [\n]{1} = \n
# ([(https){1}(http){1}]{4,5}:\/\/){1}[^\.]+[.]{1}[\w]{2,3}[\S]+ netadresse som starter med http eller https. varer helt til whitespace
