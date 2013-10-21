# this may be broken


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


class UserSample(MRJob):
    OUTPUT_PROTOCOL = RawValueProtocol
    def mapper(self, _, line):
        toks,date,geo_s,tweet_s = line.split('\t')
        tweet = json.loads(tweet_s)
        if not mrjob.util.hash_object(tweet['user']['id']).startswith('000'): return
        yield None, line

    # def reducer(self, userid, infos): #tweet_tokenizations):
    #     ntok = 0
    #     ntweet = 0
    #     counts = defaultdict(int)
    #     max_ntweet = 1e5
    #     toksample = []
    #     usernames = set()
    #     for username,toks in infos:  # tweet_tokenizations:
    #         ntweet += 1
    #         ntok += len(toks)
    #         for tok in toks:
    #             counts[tok] += 1
    #         if ntweet < 10: toksample.append(toks)
    #         if ntweet > max_ntweet: break
    #         usernames.add(username)
    #     meta = {'ntok':ntok, 'ntype':len(counts), 'ntweet':ntweet, 'usernames':list(usernames)}
    #     yield userid, [meta, {'word_counts':dict(counts), 'tweet_sample': toksample}]

if __name__=='__main__':
    UserSample.run()

