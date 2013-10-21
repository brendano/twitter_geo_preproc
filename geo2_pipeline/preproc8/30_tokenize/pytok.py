# Used for experiment, not actually used in pipeline
import sys,json
from nlp import twokenize

for line in sys.stdin:
    tweet = json.loads(line.split('\t')[-1])
    print u' '.join(twokenize.tokenize(tweet['text'])).encode('utf8')

