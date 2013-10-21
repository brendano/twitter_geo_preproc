from mrjob.job import MRJob
import mrjob.util
from mrjob.protocol import JSONValueProtocol, PickleProtocol, RawValueProtocol
import re,os,sys
# import simplejson as json
from collections import defaultdict
import json
sys.path.insert(0,'..')
from hose_util import lookup
import textproc


class Useragg(MRJob):
    def mapper(self, _, line):
        toks,date,geo_s,tweet_s = line.split('\t')
        tweet = json.loads(tweet_s)
        # if not mrjob.util.hash_object(tweet['user']['id']).startswith('0000'): return
        toks = textproc.do_tokenization(toks)
        yield tweet['user']['id'], [tweet['user']['screen_name'], toks]

    def reducer(self, userid, infos): #tweet_tokenizations):
        ntok = 0
        ntweet = 0
        unicounts = defaultdict(int)
        bicounts = defaultdict(int)
        max_ntweet = 1e5
        toksample = []
        usernames = set()
        for username,toks in infos:  # tweet_tokenizations:
            ntweet += 1
            if ntweet < max_ntweet:
                ntok += len(toks)
                for tok in toks:
                    unicounts[tok] += 1
                for i in range(len(toks)-2):
                    bigram = toks[i:(i+2)]
                    bicounts[u'_'.join(bigram)] += 1
            if ntweet < 10:
                toksample.append(toks)
            usernames.add(username)
        meta = {'ntok':ntok, 'ntype':len(unicounts), 'ntweet':ntweet, 'usernames':list(usernames)}
        yield userid, [meta, {'unigram_counts':dict(unicounts), 'bigram_counts':dict(bicounts),
            'tweet_sample': toksample}]

if __name__=='__main__':
    Useragg.run()

