import re,sys,os,itertools
import ujson as json

## Umm, try to replicate config in 50_quadify ...
OPTS = {}
OPTS['min_date'] = '2009-08-03'
OPTS['max_date'] = '2012-09-30'
OPTS['msa_county_file'] = os.path.join(os.path.dirname(__file__), '../../../geo_metro/msa_counties.tsv')
OPTS['num_msas'] = 200

countyfips2regionid = {}
for line in open(OPTS['msa_county_file']).readlines()[1:]:
    rank,name,countyfips = line.split('\t')
    rank = int(rank)
    if rank > OPTS['num_msas']: continue
    countyfips = countyfips.strip().split(',')
    for fips in countyfips:
        countyfips2regionid[fips] = rank
def get_region(geodict):
    county_fips = geodict['us_county']['geoid10']
    return countyfips2regionid.get(county_fips, None)

def iterate_tweets():
    for line in sys.stdin:
        parts = line.rstrip('\n').split('\t')
        date,user,geo,tweet = parts
        date = date.split('T')[0]
        if date < OPTS['min_date'] or date > OPTS['max_date']:
            continue
        region = get_region(json.loads(geo))
        if region is None:
            continue
        yield user, tweet.split()

def stuff():
    for user, tweets in itertools.groupby(iterate_tweets(), key=lambda (u,t): u):
        wordset = set()
        for _,toks in tweets:
            for tok in toks:
                wordset.add(tok)
        for word in wordset:
            print word

stuff()
