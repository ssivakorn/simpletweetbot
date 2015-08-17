#!/usr/bin/python
import sys
import os
import time
import getopt
import random
import datetime
import argparse
import xml.etree.ElementTree as ET

# tweepy lib
import tweepy
# constants
MIN = 60
def get_curr_time():
    """ get current time in string: year-month-date hour:min:sec
    """
    return datetime.datetime.now().strftime('[%Y-%m-%d %H:%M:%S] ')

def read_args():
    """ read argument
    """
    secretkey = None
    tweettxt = None
    mininterval = 0 # min
    rand = False

    parser = argparse.ArgumentParser(description="tweetbot: automate tweet")
    parser.add_argument('-t', '--tweettxt', required=True,
                        help="tweettxt file")
    parser.add_argument('-r', '--random', action='store_true',
                        help="random tweet from tweettxt file")
    parser.add_argument('-s', '--secretkey', required=True,
                        help="tweeter api secret key file")
    parser.add_argument('-i', '--interval', default=15,
                        help="sleep interval between each tweet, \
                                default is 15 minutes")

    args = parser.parse_args()
    tweettxt = args.tweettxt
    secretkey = args.secretkey
    rand = args.random
    mininterval = int(args.interval) * MIN

    return (secretkey, tweettxt, mininterval, rand)

def _read_secrets(secretkey_file):
    """ read secretkey from xml
    """
    tree = ET.parse(secretkey_file)
    root = tree.getroot()

    api = root.find('api')
    api_key = api.find('key').text
    api_secret = api.find('secret').text

    accesstoken	= root.find('accesstoken')
    accesstoken_key = accesstoken.find('key').text
    accesstoken_secret = accesstoken.find('secret').text

    return (api_key, api_secret, accesstoken_key, accesstoken_secret)

def _tweet(status, image=""):
    """ tweet status (and image)
    status:	tweet status
    image:	tweet image

    """
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

def tweetbot(tweettxt_f, mininterval, random_on):
    # open tweettxt file
    tree = ET.parse(tweettxt_f)
    tweets = tree.getroot()

    # random function on
    if random_on:
        while True:
            random_num = random.randint(0, int(len(tweets)) - 1)
            tweet = tweets[random_num]
            # call tweet
            tw_status = _tweet(tweet.get('txt'), tweet.get('img'))

            # sleep for given interval
            if tw_status:
                time.sleep(int(mininterval))

    # random function off
    else:
        for tweet in tweets:
            # call tweet
            tw_status = _tweet(tweet.get('txt'), tweet.get('img'))
            if tw_status:
                # sleep for given interval
                time.sleep(mininterval)

if __name__ == "__main__":

    (secretkey_f, tweettxt_f,
            mininterval, rand) = read_args()
    (api_key, api_secret,
     accesstoken_key, accesstoken_secret) = _read_secrets(secretkey_f)

    print "[*] SETUP INFO"
    print "\tapi key: %s" % api_key
    print "\tapi secret: %s" % api_secret
    print "\taccess token key: %s" % accesstoken_key
    print "\taccess token secret: %s" % accesstoken_secret
    print "\ttweet text file: %s" % tweettxt_f
    print "\tinterval: %d seconds" % mininterval
    print "\trandom order: %s" % rand

    # auth tweeter
    api = _tweeter_auth(api_key,
                        api_secret,
                        accesstoken_key,
                        accesstoken_secret)

    tweetbot(tweettxt_f, mininterval, rand)





