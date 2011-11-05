import sys,os,time,re

for m in ['json','simplejson','yajl','ujson']:
  try:
    exec "import %s as json" % m
  except ImportError:
    pass

from datetime import datetime,timedelta
from collections import defaultdict
from types import DictType
from pprint import pprint

def iterate(raw=False, filters=True):
  """
  Iterate through tweets on stdin, skipping junk.
  """
  num_valid = 0
  has_id = 0
  seen_dates = set()
  for i,line in enumerate(sys.stdin):
    try:
      myjson = json.loads(line)
      if not isinstance(myjson,dict): raise ValueError("bad line")
      num_valid += 1
      has_id += ('id' in myjson)
      if filters and ('text' not in myjson or 'created_at' not in myjson):
        continue
      if 'created_at' in myjson:
        d = get_date(myjson)
        ymd = d.strftime("%Y-%m-%d")
        seen_dates.add(ymd)
        myjson['created_at_datetime'] = d
        myjson['created_at_ymd'] = ymd
      if raw:
        yield line.strip(), myjson
      else:
        yield myjson
    except ValueError, e:
      pass
      #print>>sys.stderr, "bad myjson object: ", line
    if False and ((i+1) % 100000) == 0:
      print>>sys.stderr, "TWEET ITER: %d processed, %d valid, %d with id" % (i+1, num_valid, has_id)
      if len(seen_dates) > 10:
        print>>sys.stderr, "\t%d seen dates" % (len(seen_dates))
      else:
        print>>sys.stderr, "\tSeen dates: %s" % (sorted(list(seen_dates)),)

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
