from mrjob.job import MRJob
import mrjob.util
from mrjob.protocol import JSONValueProtocol, PickleProtocol, RawValueProtocol
import sys,json
sys.path.insert(0, '..')
import textproc

def dumps(obj):
    return json.dumps(obj, separators= (',', ':'))

def smallify(toktweet_line):
    toks, date, geo_s, tweet_s = toktweet_line.split('\t')
    toks = textproc.do_tokenization(toks)
    geo = json.loads(geo_s)
    tweet = json.loads(tweet_s)
    userid = tweet['user']['id']
    # tweetid = tweet.get('id_str')
    # if not tweetid: tweetid = str(tweet['id'])
    tweetid = tweet['id']
    # return {'date':date,'id':tweetid,'userid':userid,'geo':geo,'tokens':toks}
    return [date, str(userid), dumps(geo), ' '.join(toks)]

class MyJob(MRJob):
    OUTPUT_PROTOCOL = RawValueProtocol
    def mapper(self, _, line):
        smalltweet = smallify(line)
        yield smalltweet[1], '\t'.join(smalltweet)
    def reducer(self, userid, smalltweets):
        for smalltweet in smalltweets:
            yield None, smalltweet

if __name__=='__main__':
    MyJob.run()

# for line in sys.stdin:
#     d = smallify(line)
#     # print dumps(d)
#     print '\t'.join([d['date'],d['id'],str(d['userid']), dumps(d['geo']), ' '.join(d['tokens']) ])
