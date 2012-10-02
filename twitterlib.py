#-*- coding: utf-8 -*-


import math
import re
import tweepy
import time

def getUserId(screen_name,table,last_time):
    if table.has_key(screen_name):
        return (table[screen_name],last_time)
    elif time.time()-last_time>3600:
        try:
            user=tweepy.api.get_user(screen_name)
        except tweepy.error.TweepError, e:
            if e.response.status==404:
                print screen_name
                table[screen_name]="@"+screen_name
                return ("@"+screen_name, last_time)
            elif e.response.status==400:
                print "Rate limit exceeded"
                return ("@"+screen_name, time.time())
            else:
                print e.response.status
                raise
        table[screen_name]=str(user.id)
        return (str(user.id), last_time)
    else:
        print "Rate limit exceeded %d min ago. Still waiting" % ((time.time()-last_time)/60)
        return ("@"+screen_name, last_time)


def countValidTweets(file):
    count=0;
    total=0;
    for line in open(file):
        total+=1
        line=line.rstrip('\r\n')
        tmp=line.split('\t')
        mentions=tmp[3].split(',')
        count += False not in map((lambda x: len(x)==0 or x[0]!='@'),mentions)
    return (count,total)

def getMentions(text,table):
    pMention=re.compile('@[a-z0-9A-Z_]{1,15}')
    links = pMention.findall(text)
    for i,link in enumerate(links):
        if table.has_key(link[1:]):
            links[i]=table[link[1:]]
        else:
            print link[1:]
            links[i]=link
    return links

def loadUserIdScreenNameTable(file):
    table={}
    for line in open(file):
        line=line.rstrip('\r\n')
        tmp=line.split(',')
        table[tmp[1]]=tmp[0]
    return table
