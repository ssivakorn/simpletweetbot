# Simple Tweetbot
Small and Simple time-based auto tweet client for twitter user, written in Python with Tweepy Library

Features:

* Auto tweet -- adjustable interval in second e.g. tweet every hour
* Written in Python, Easy! and Portable!
* Easy adjustable tweet status and image in xml

## Installation

* Install Tweepy Library
```bash
$ pip install tweepy
```

* Download
```bash
$ git clone git@github.com:ssivakorn/simpletweetbot.git
```
* Configure tw_secret.xml. Get your own API and access token from https://apps.twitter.com/
```xml
<?xml version="1.0"?>
<setup>
<api>
<key>YOUR_API_KEY</key>
<secret>YOUR_API_SECRET</secret>
</api>
<accesstoken>
<key>YOUR_ACCESS_TOKEN</key>
<secret>YOUR_ACCESS_TOKEN_SECRET</secret>
</accesstoken>
</setup>
```
* Personalize your tweet status and image in tw_text.xml and (optional) put any sample image in images directory 
```xml
<?xml version="1.0"?>
<data>
<tweet txt="hello world here is your #tweet text" img="./images/helloworld.gif" />
</data>
```
status tag:
```
txt="YOUR STATUS"
```
images tag:
```
img="PATH TO YOUR IMAGE"
```
* Done!

## Start Running

```bash
$ python tweetbot.py -s <xml_secret_key_file> -t <tweet_txt_file> -i <interval_in_second> -r
```
Supplied Arguments:

* -s xml_secret_key_file
* -t xml_tweet_text_file
* -i time interval (interval between each tweet status in second)
* -r randomly tweet status (not follow the order in tweet_text_file)

This manual is made by (GitHub-Flavored) Markdown Editor: http://jbt.github.io/markdown-editor/
