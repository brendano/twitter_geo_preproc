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
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
import tsutil


OPTS = {}

# Define time.  try to start on Monday, end on Sunday.
OPTS['min_date'] = '2009-08-03'
OPTS['max_date'] = '2012-09-30'

# Define regions
OPTS['msa_county_file'] = os.path.join(os.path.dirname(__file__), '../../../geo_metro/msa_counties.tsv')
OPTS['num_msas'] = 202

# Define words
OPTS['word_vocab_file'] = os.path.join(os.path.dirname(__file__), 'smalltweets2.word_usercount.topsort')
OPTS['num_words'] = int(100e3)

# Input/Output
OPTS['num_word_buckets'] = 100
import argparse
p = argparse.ArgumentParser()
p.add_argument('input_dir')
p.add_argument('output_dir')
ARGS = p.parse_args()

assert os.path.exists(ARGS.input_dir)

os.system("mkdir -p " + ARGS.output_dir)
log_fp = open(os.path.join(ARGS.output_dir, 'quadify.log'), 'w')

def outpath(filename):
    f = os.path.join(ARGS.output_dir, filename)
    if not os.path.exists(os.path.dirname(f)):
        os.system("mkdir -p " + os.path.dirname(f))
    return f

def log(msg):
    print msg
    print>>log_fp, msg
    log_fp.flush()

def save_logfile():
    log_fp.close()

class Numberizer(OrderedDict):
  def num(self, ob):
    if ob not in self:
      self[ob] = len(self) + 1   # +1  ==>  1-indexed
    return self[ob]

#### Main ####

quadify_start = datetime.now()
log("Started {}\nOPTS\t{}\nARGS\t{}".format(quadify_start, json.dumps(OPTS), repr(ARGS)))

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

with open(outpath('date_info'), 'w') as f:
    for d in alldates:
        print>>f, "{}\t{}\t{}".format(
                d.strftime("%Y-%m-%d"), 
                json.dumps(date_to_yearweek[d]),
                date_to_timeid[d])

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

def get_timeid(datestr):
    dt = datetime.strptime(datestr, '%Y-%m-%dT%H:%M:%S')
    # dt = datetime(dt.year, dt.month, dt.day)  # Naive UTC midnight cutpoint
    dt = get_crossusa_day(dt)
    return date_to_timeid.get(dt, None)


## Region IDs
countyfips2regionid = {}
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

log("{} counties for {} MSAs".format(
    len(countyfips2regionid.keys()),
    len(set(countyfips2regionid.values()))))

# print countyfips2regionid

## Word IDs
word_to_wordid = Numberizer()
for line in open(OPTS['word_vocab_file']):
    word = line.split()[0]
    assert word not in word_to_wordid
    wordid = word_to_wordid.num(word)
    if wordid >= OPTS['num_words']:
        break

with open(outpath('word_info'), 'w') as f:
    for word,wordid in word_to_wordid.iteritems():
        print>>f, "{}\t{}".format(word, wordid)

## User vocab... we make it internally.  Remember to output at end.
userstr_to_userid = Numberizer()
def save_user_info():
    log("saving user info")
    with open(outpath('user_info'),'w') as f:
        for userstr, userid in userstr_to_userid.iteritems():
            print>>f, "{}\t{}".format(userstr, userid)



### Do the actual processing now
def iterate_smalltweets():
    for filename in glob.glob("{}/part*".format(ARGS.input_dir)):
        log("processing " + filename)
        for line in open(filename):
            parts = line.rstrip('\n').split('\t')
            yield {'date':parts[0],
                    'user': parts[1],
                    'geo':json.loads(parts[2]),
                    'tokens':parts[3].split()
            }

def get_region(tweet):
    county_fips = tweet['geo']['us_county']['geoid10']
    return countyfips2regionid.get(county_fips, None)

# Set up output files
OUT = {}
for wb in range(OPTS['num_word_buckets']):
    OUT['quints','wb',wb] =   open(outpath('quints/wb=%03d' % wb), 'w')

def get_wordbucket_file(wordid):
    wb = wordid % OPTS['num_word_buckets']
    return OUT['quints','wb',wb]

def close_wordbucket_files():
    for key,fp in OUT.items():
        fp.close()

def progress(userid):
    if userid % 1000 == 0:
        sys.stderr.write(".")
    if userid % 100000 == 0 or userid==10000:
        s = (datetime.now() - quadify_start).seconds
        print>>sys.stderr, " {} users seen; {} users/hr".format(userid, userid / (s/3600))

log("Starting main pass, creating quints")

num_tweets_input = 0
num_tweets_used = 0
usercount_by_timeregion = Counter()  ##  (t,r) => num users with at least one tweet there

for user, user_tweets in itertools.groupby(iterate_smalltweets(), key=lambda d: d['user']):
    userid = userstr_to_userid.num(user)
    progress(userid)

    time_region_word_counts = Counter()
    timeregions_user_has_touched = set()  ## (t,r) pairs where user has at least one nonempty tweet
    for tweet in user_tweets:
        num_tweets_input += 1
        regionid = get_region(tweet)
        if regionid is None:
            # print "reject", tweet['geo']
            continue
        timeid = get_timeid(tweet['date'])
        if timeid is None:
            # print "reject", tweet['date']
            continue

        tokens = [token for token in tweet['tokens'] if token in word_to_wordid]
        # if not tokens: 
        #     # print "reject empty"
        #     continue

        # Tweet has passed the filters.
        num_tweets_used += 1
        timeregions_user_has_touched.add((timeid,regionid))
        for token in tokens:
            time_region_word_counts[(timeid,regionid,token)] += 1

    for timeid,regionid in timeregions_user_has_touched:
        usercount_by_timeregion[timeid,regionid] += 1

    for (timeid,regionid,word),count in time_region_word_counts.iteritems():
        wordid = word_to_wordid[word]
        row = [timeid, regionid, userid, wordid, count]
        print>>get_wordbucket_file(wordid), '\t'.join(str(x) for x in row)

close_wordbucket_files()

log("Scan through SmallTweets files is complete.")
log("{} tweets input, {} tweets used".format(num_tweets_input, num_tweets_used))

log("Saving time,region,usercount info")
with open(outpath("time_region_usercount"),'w') as f:
    items = usercount_by_timeregion.items()
    items.sort(key= lambda ((t,r),c): (r,t))
    for (timeid,regionid),count in items:
        print>>f, '\t'.join(str(x) for x in [timeid, regionid, count])

save_user_info()

log("Rolling up to quads")
for infile in glob.glob(outpath("quints/wb=*")):
    sys.stderr.write(".")
    outfile = outpath("quads/" + os.path.basename(infile))
    # print infile, "==>", outfile
    timeregionword_usercounts = Counter()
    for line in open(infile):
        # print repr(line)
        timeid,regionid,userid,wordid,count = [int(x) for x in line.split('\t')]
        timeregionword_usercounts[timeid,regionid,wordid] += 1
    with open(outfile,'w') as outfp:
        for (timeid,regionid,wordid),count in timeregionword_usercounts.items():
            print>>outfp, '\t'.join(str(x) for x in [timeid,regionid,wordid,count])
sys.stderr.write("\n")

log("Ended {} ({} elapsed)".format(datetime.now(), datetime.now() - quadify_start))
save_logfile()

