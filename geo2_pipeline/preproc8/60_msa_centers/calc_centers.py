from __future__ import division
import sys,os,glob,itertools,re
try:
    import ujson as json
except ImportError:
    import json
# from counter import counter
from datetime import datetime, timedelta
from collections import Counter
from collections import OrderedDict
from collections import defaultdict
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
import tsutil

class Numberizer(OrderedDict):
  def num(self, ob):
    if ob not in self:
      self[ob] = len(self) + 1   # +1  ==>  1-indexed
    return self[ob]


OPTS = {}

# Define time.  try to start on Monday, end on Sunday.
OPTS['min_date'] = '2009-08-03'
OPTS['max_date'] = '2012-09-30'

OPTS['msa_county_file'] = os.path.join(os.path.dirname(__file__), '../../../geo_metro/msa_counties.tsv')
OPTS['num_msas'] = 202

# import argparse
# p = argparse.ArgumentParser()
# p.add_argument('input_dir')
# ARGS = p.parse_args()

# log_fp = sys.stdout
def log(msg):
    print msg
    # print>>log_fp, msg
    # log_fp.flush()


## Region IDs
countyfips2regionid = {}
regionid2msaname = {}
for line in open(OPTS['msa_county_file']).readlines()[1:]:
    rank,name,countyfips = line.split('\t')
    if re.search(r'\b(AK|HI)\b', name):
        log("removing MSA " + name)
        continue
    rank = int(rank)
    if rank > OPTS['num_msas']: continue
    countyfips = countyfips.strip().split(',')
    for fips in countyfips:
        countyfips2regionid[fips] = rank
    regionid2msaname[rank] = name

log("{} counties for {} MSAs".format(
    len(countyfips2regionid.keys()),
    len(set(countyfips2regionid.values()))))

### Do the actual processing now
def iterate_smalltweets():
    # for filename in glob.glob("{}/part*".format(ARGS.input_dir)):
    #     log("processing " + filename)
    for line in sys.stdin:
        parts = line.rstrip('\n').split('\t')
        yield {'date':parts[0],
                'user': parts[1],
                'geo':json.loads(parts[2]),
                'tokens':parts[3].split()
        }

def get_crossusa_day(utc_dt):
    """
    "cross-usa day" starting at UTC 0800  (4am/3am EDT/EST, 1am/12am PDT/PST)
    Intended to be a single real timepoint that reasonably divides days in all
    of the lower48 of the USA.  In other words, it's the PST day.
    PST date d at 12:01am == UTC date d, 0801
    EDT date d at  4:01am == UTC date d, 0801
    PST date d at 11:30pm == UTC date d+1, 0730
    UTC date d, 0801 ==> cross-usa date is d
    UTC date d, 0759 ==> cross-usa date is d-1
    """
    d = datetime(utc_dt.year, utc_dt.month, utc_dt.day)
    if utc_dt.hour < 8:
        d = d - timedelta(days=1)
    return d

## Time IDs
alldates = []
d1 = datetime.strptime(OPTS['min_date'], '%Y-%m-%d')
d2 = datetime.strptime(OPTS['max_date'], '%Y-%m-%d')
d = d1
while d <= d2:
    alldates.append(d)
    d = d + timedelta(days=1)

yearweek_to_timeid = Numberizer()
date_to_yearweek = {}
date_to_timeid = {}
for d in alldates:
    y,w = tsutil.rollup_bucket['week'](d)
    date_to_yearweek[d] = (y,w)
    timeid = yearweek_to_timeid.num((y,w))
    date_to_timeid[d] = timeid

def get_timeid(datestr):
    dt = datetime.strptime(datestr, '%Y-%m-%dT%H:%M:%S')
    # dt = datetime(dt.year, dt.month, dt.day)  # Naive UTC midnight cutpoint
    dt = get_crossusa_day(dt)
    return date_to_timeid.get(dt, None)

def get_region(tweet):
    county_fips = tweet['geo']['us_county']['geoid10']
    return countyfips2regionid.get(county_fips, None)


sums_by_regionid = defaultdict(lambda: {'n':0, 'lon':0, 'lat':0})
# from kahan import Kahan
# sums_by_regionid = defaultdict(lambda: {'n':0, 'lon':Kahan(), 'lat':Kahan()})

for user, user_tweets in itertools.groupby(iterate_smalltweets(), key=lambda d: d['user']):
    # userid = userstr_to_userid.num(user)
    # progress(userid)

    # basically dividing up a user into multiple versions per unique region
    lonlat_by_regionid = defaultdict(list)
    for tweet in user_tweets:
        # num_tweets_input += 1
        regionid = get_region(tweet)
        if regionid is None:
            # print "reject", tweet['geo']
            continue
        timeid = get_timeid(tweet['date'])
        if timeid is None:
            # print "reject", tweet['date']
            continue
        lonlat_by_regionid[regionid].append(tweet['geo']['lonlat'])
    for regionid,lonlats in lonlat_by_regionid.items():
        n = len(lonlats)
        if not n: continue
        sums_by_regionid[regionid]['lon'] += sum(lon for lon,lat in lonlats) / n
        sums_by_regionid[regionid]['lat'] += sum(lat for lon,lat in lonlats) / n
        sums_by_regionid[regionid]['n'] += 1

print "FINAL OUTPUT"
# print sums_by_regionid
for regionid, d in sorted(sums_by_regionid.items()):
    print '\t'.join([str(x) for x in [
        regionid, d['lon']/d['n'], d['lat']/d['n'], d['n'], regionid2msaname[regionid]]])



