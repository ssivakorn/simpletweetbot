#!/usr/bin/python
import sys
import os
import time
import getopt
import random
import xml.etree.ElementTree as ET
# tweepy lib
import tweepy

# options and arguments
USAGE = 'auto_tweet.py ' + \
		'-s <xml_secret_key_file> ' + \
		'-t <tweet_txt_file> ' + \
		'-i <interval_in_second>' + \
		'-r'

# func: read from command line arguments
def readopts(argv):
	secretkey_file = ''
	tweettxt_file = ''
	interval = ''
	random_on = False

	if not argv:
		print USAGE
		sys.exit(2)

	try:
		opts, args = getopt.getopt(argv, 'hrs:t:i:', ['help', 'random', 'secretkey=', 'tweettxt=', 'intvl='])
	except getopt.GetoptError:
		print USAGE
		sys.exit(2)

	for opt, arg in opts:
		if opt in ('-h', '--help'):
			print USAGE
			sys.exit(0)
		elif opt in ('-r', '--random'):
			random_on = True
		elif opt in ('-s', '--secretkey'):
			secretkey_file = arg
		elif opt in ('-t', '--tweettxt'):
			tweettxt_file = arg
		elif opt in ('-i' , '--interval'):
			interval = arg

	return [secretkey_file, tweettxt_file, interval, random_on]

# func: read secretkey from xml
def read_secrets(secretkey_file):
	tree = ET.parse(secretkey_file)
	root = tree.getroot()
	
	api 		= root.find('api')
	api_key 	= api.find('key').text
	api_secret	= api.find('secret').text

	accesstoken			= root.find('accesstoken')
	accesstoken_key		= accesstoken.find('key').text
	accesstoken_secret	= accesstoken.find('secret').text

	return [api_key, api_secret, accesstoken_key, accesstoken_secret]


# func: tweet status (and image)
# @status:	tweet status
# @image:	tweet image
def tweet_(status, image):
	try:
		if len(image) > 1:
			print 'POSTING: ' + status + ' -- ' + image
			api.update_with_media(image, status=status)	
		else:
			print 'POSTING: ' + status
			api.update_status(status)

	except Exception, e:
		print repr(e)

# main program
opts = readopts(sys.argv[1:])
secretkey_file 	= opts[0]
tweettxt_file  	= opts[1]
interval		= opts[2]
random_on		= opts[3]

secrets = read_secrets(secretkey_file)
API_KEY 	= secrets[0]
API_SECRET	= secrets[1]
ACCESSTOKEN_KEY 		= secrets[2]
ACCESSTOKEN_SECRET 	= secrets[3]


print "API_KEY: \t\t" + API_KEY
print "API_SECRET: \t\t" + API_SECRET
print "ACCESSTOKEN_KEY: \t" + ACCESSTOKEN_KEY
print "ACCESSTOKEN_SECRET: \t" + ACCESSTOKEN_SECRET
print "TWEET FILE: \t\t" + tweettxt_file
print "INTERVAL: \t\t" + interval

auth = tweepy.OAuthHandler(API_KEY, API_SECRET)
auth.set_access_token(ACCESSTOKEN_KEY, ACCESSTOKEN_SECRET)
api = tweepy.API(auth)

tree = ET.parse(tweettxt_file)
tweets = tree.getroot()

# random function on
if random_on:
	while(True):
		random_num = random.randint(0, int(len(tweets)) - 1)	
		tweet = tweets[random_num]
		# call tweet
		tweet_(tweet.get('txt'), tweet.get('img'))

		# sleep for given interval
		time.sleep(int(interval))

# random function off
else:
	for tweet in tweets:
		# call tweet
		tweet_(tweet.get('txt'), tweet.get('img'))
		
		# sleep for given interval
		time.sleep(int(interval))
