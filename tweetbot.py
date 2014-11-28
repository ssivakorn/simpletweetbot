#!/usr/bin/python
import sys
import os
import time
import getopt
import random
import datetime
import xml.etree.ElementTree as ET
# tweepy lib
import tweepy

# options and arguments
USAGE = sys.argv[0] + " " + \
		'-s <xml_secret_key_file> ' + \
		'-t <tweet_txt_file> ' + \
		'-i <interval_in_second> ' + \
		'-r'

# func: get current date and time
def get_curr_time():
    return datetime.datetime.now().strftime('[%Y-%m-%d %H:%M:%S] ')	

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

    return (secretkey_file, tweettxt_file, interval, random_on)

# func: read secretkey from xml
def _read_secrets(secretkey_file):
    tree = ET.parse(secretkey_file)
    root = tree.getroot()

    api = root.find('api')
    api_key = api.find('key').text
    api_secret = api.find('secret').text

    accesstoken	= root.find('accesstoken')
    accesstoken_key = accesstoken.find('key').text
    accesstoken_secret = accesstoken.find('secret').text

    return (api_key, api_secret, accesstoken_key, accesstoken_secret)


# func: tweet status (and image)
# @status:	tweet status
# @image:	tweet image
def _tweet(status, image=""):
    try:
        print '[+] POSTING: ' + get_curr_time() + status + ' -- ' + image
        if image:
            api.update_with_media(image, status=status)	
        else:
            api.update_status(status)

    except Exception, e:
        print repr(e)
        return False
    return True

def _tweeter_auth(api_key, api_secret, accesstoken_key, accesstoken_secret):
    auth = tweepy.OAuthHandler(api_key, api_secret)
    auth.set_access_token(accesstoken_key, accesstoken_secret)
    return tweepy.API(auth)

def tweetbot(tweettxt_f, random_on=False):

    # open tweettxt file
    tree = ET.parse(tweettxt_f)
    tweets = tree.getroot()

    # random function on
    if random_on:
        while (True):
            random_num = random.randint(0, int(len(tweets)) - 1)	
            tweet = tweets[random_num]
            # call tweet
            tw_status = _tweet(tweet.get('txt'), tweet.get('img'))

            if tw_status:
                # sleep for given interval
                time.sleep(int(interval))

    # random function off
    else:
        for tweet in tweets:
            # call tweet
            tw_status = _tweet(tweet.get('txt'), tweet.get('img'))		
            if tw_status:
                # sleep for given interval
                time.sleep(int(interval))

# main program
if __name__ == "__main__":
    (secretkey_f, tweettxt_f, interval, random_on)= readopts(sys.argv[1:])
    (api_key, api_secret,
     accesstoken_key, accesstoken_secret) = _read_secrets(secretkey_f)

    print "API_KEY: \t\t" + api_key
    print "API_SECRET: \t\t" + api_secret
    print "ACCESSTOKEN_KEY: \t" + accesstoken_key
    print "ACCESSTOKEN_SECRET: \t" + accesstoken_secret
    print "TWEET FILE: \t\t" + tweettxt_f
    print "INTERVAL: \t\t" + interval

    # auth tweeter
    api = _tweeter_auth(api_key, api_secret,
                        accesstoken_key, accesstoken_secret)

    tweetbot(tweettxt_f, random_on)





