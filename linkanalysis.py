#-*- coding: utf-8 -*-


import twitterlib
import sys


def output(fo, tweet_id, user_id, timestamp, body, table):
    links=twitterlib.getMentions(body,table)
    links=",".join(links)
    fo.write('%s\t%s\t%s\t%s\n' % (tweet_id, user_id, timestamp, links))

tweet_id=''
user_id=''
timestamp=''
body=''

userid_file = '/data/shinsaidata/twitter/userid-screenname'

table=twitterlib.loadUserIdScreenNameTable(userid_file)

fo = open(sys.argv[2],'w')

kk=0;
for line in open(sys.argv[1]):
    kk+=1
    line = line.rstrip('\r\n')
    fields = line.split('\x01')
    if len(fields)>=4:
        if tweet_id:
            output(fo, tweet_id, user_id, timestamp, body, table)
        tweet_id = fields[0]
        user_id  = fields[1]
        timestamp=fields[2]
        body = '\x01'.join(fields[3:])
    else:
        body += '\\n' + line

if tweet_id:
    output(fo, tweet_id, user_id, timestamp, body, table)

