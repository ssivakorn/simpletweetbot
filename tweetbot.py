#!/usr/bin/python
import sys
import os
import tweepy
import time
import getopt
import xml.etree.ElementTree as ET

# options and arguments
USAGE = 'auto_tweet.py ' + \
	'-s <xml_secret_key_file> ' + \
	'-t <tweet_txt_file> ' + \
	'-i <interval_in_second>'

# read from command line arguments
def readopts(argv):
    secretkey_file = ''
    tweettxt_file = ''
    interval = ''

    if not argv:
        print USAGE
        sys.exit(2)

    try:
	opts, args = getopt.getopt(argv, 'hs:t:i:', ['help', 'secretkey=', 'tweettxt=', 'intvl='])
    except getopt.GetoptError:
	print USAGE
	sys.exit(2)

    for opt, arg in opts:
	if opt in ('-h', '--help'):
	    print USAGE
	    sys.exit(0)
	elif opt in ('-s', '--secretkey'):
	    secretkey_file = arg
	elif opt in ('-t', '--tweettxt'):
	    tweettxt_file = arg
	elif opt in ('-i' , '--interval'):
	    interval = arg

    return [secretkey_file, tweettxt_file, interval]

# read secretkey from xml
def readsecrets(secretkey_file):
	tree = ET.parse(secretkey_file)
	root = tree.getroot()
	
	api 		= root.find('api')
	api_key 	= api.find('key').text
	api_secret	= api.find('secret').text

	accesstoken			= root.find('accesstoken')
	accesstoken_key		= accesstoken.find('key').text
	accesstoken_secret	= accesstoken.find('secret').text

	return [api_key, api_secret, accesstoken_key, accesstoken_secret]

# main
opts = readopts(sys.argv[1:])
secretkey_file 	= opts[0]
tweettxt_file  	= opts[1]
interval		= opts[2]

secrets = readsecrets(secretkey_file)
API_KEY 	= secrets[0]
API_SECRET	= secrets[1]
ACCESSTOKEN_KEY 		= secrets[2]
ACCESSTOKEN_SECRET 	= secrets[3]


print "API_KEY: " + API_KEY
print "API_SECRET: " + API_SECRET
print "ACCESSTOKEN_KEY: " + ACCESSTOKEN_KEY
print "ACCESSTOKEN_SECRET: " + ACCESSTOKEN_SECRET
print "TWEET FILE: " + tweettxt_file
print "INTERVAL: " + interval

auth = tweepy.OAuthHandler(API_KEY, API_SECRET)
auth.set_access_token(ACCESSTOKEN_KEY, ACCESSTOKEN_SECRET)
api = tweepy.API(auth)

tree = ET.parse(tweettxt_file)
root = tree.getroot()

for tweet in root:
	status = tweet.get('txt')
	media = tweet.get('img')
	
	try:
		if len(media) > 1:
			print 'POSTING: ' + status + ' ** ' + media
			api.update_with_media(media, status=status)	
		else:
			print 'POSTING: ' + status
			api.update_status(status)

		time.sleep(int(interval))

	except Exception, e:
		print "ERROR: " + e.message

'''
#filename = open(tweettxt_file, 'r')
#f = filename.readlines()
#filename.close()

for line in f:
	#api.update_status(line)
	#print line
	
	strings = line.split(' -- ',2)
	status = strings[0]
	
	if len(strings) > 1:
		media = strings[1].strip()
		print 'POSTING: ' + status + ' ** ' + media
		print media
		api.update_with_media(media, status=status)	
	else:
		print 'POSTING: ' + status
		api.update_status(status)

		time.sleep(interval)
'''
