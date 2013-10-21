#!/usr/bin/env python

import sys,os,time,re

import json
# Try to get a faster json library
# simplejson is usually slightly faster than 'json'
# ujson has bug with >32bit integers
# yajl has memory leak with encoding, but decoding seems ok
# for m in ['simplejson','yajl']:
#   try:
#     exec "import %s as json" % m
#   except ImportError:
#     pass

from datetime import datetime,timedelta
from collections import defaultdict
from types import DictType
from pprint import pprint

seen_dates = set()

def iterate(raw=False, filters=True):
  """
  Iterate through tweets on stdin, skipping junk.
  """
  global seen_dates
  num_valid = 0
  has_id = 0
  for i,line in enumerate(sys.stdin):
    try:
      myjson = json.loads(line)
      if not isinstance(myjson,dict): raise ValueError("bad line")
      num_valid += 1
      has_id += ('id' in myjson)
      if filters and ('text' not in myjson or 'created_at' not in myjson):
        continue
      enhance_tweet(myjson)
      if raw:
        yield line.strip(), myjson
      else:
        yield myjson
    except ValueError, e:
      pass
      #print>>sys.stderr, "bad myjson object: ", line
    if ((i+1) % int(1e6)) == 0:
      print>>sys.stderr, "TWEET ITER: %d processed, %d valid, %d with id" % (i+1, num_valid, has_id)
      if len(seen_dates) > 10:
        print>>sys.stderr, "\t%d seen dates" % (len(seen_dates))
      else:
        print>>sys.stderr, "\tSeen dates: %s" % (sorted(list(seen_dates)),)

def enhance_tweet(myjson):
    global seen_dates
    if 'created_at' in myjson:
        d = get_date(myjson)
        ymd = d.strftime("%Y-%m-%d")
        seen_dates.add(ymd)
        myjson['created_at_datetime'] = d
        myjson['created_at_ymd'] = ymd
        myjson['created_at_iso'] = d.strftime("%Y-%m-%dT%H:%M:%S")

def lookup(myjson, k):
  # return myjson[k]
  if '.' in k:
    # jpath path
    ks = k.split('.')
    v = myjson
    for k in ks: v = v.get(k,{})
    return v or ""
  return myjson.get(k,"")

def parse_date(twitter_lame_datetime_string):
  # e.g. the 'created_at' field
  return time.strptime(twitter_lame_datetime_string, "%a %b %d %H:%M:%S +0000 %Y")

def get_date(myjson_object):
  if 'created_at' not in myjson_object: return None
  return datetime(*parse_date(myjson_object['created_at'])[:7])

#datetime(*t[:7]).strftime("%Y-%m-%d")

WS = re.compile(r'[ \t\r\n]+', re.U)
def ws_norm(s):
  return unicodify(WS.sub(' ',stringify(s)))

def unicodify(s, encoding='utf8', *args):
  if isinstance(s,unicode): return s
  if isinstance(s,str): return s.decode(encoding, *args)
  return unicode(s)

def stringify(s, encoding='utf8', *args):
  if isinstance(s,str): return s
  if isinstance(s,unicode): return s.encode(encoding, *args)
  return str(s)


def tabjoin(*args):
  return u'\t'.join(unicodify(x) for x in args).encode('utf-8')

def uniq_c(seq):
  ret = defaultdict(lambda:0)
  for x in seq:
    ret[x] += 1
  return dict(ret)

def commaize(num):
  num = list(str(num))
  blocks = []
  while num:
    blocks.append( num[-3:] )
    num = num[:-3]
  blocks = ["".join(x) for x in reversed(blocks)]
  return ",".join(blocks)


if __name__=='__main__':
    # print>>sys.stderr, "json module is", json
    fields = ['id','created_at_iso','user.screen_name','text']
    for raw,tweet in iterate(raw=True):
        record = [unicodify(lookup(tweet, f)) for f in fields]
        record = [ws_norm(x) for x in record]
        record.append(raw)
        print u'\t'.join(record).encode('utf-8')

