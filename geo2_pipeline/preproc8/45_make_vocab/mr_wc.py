from mrjob.job import MRJob
import re,sys

def usergrouper_map(_, line):
    parts = line.split('\t')
    userid,toks = parts[1], parts[-1]
    yield userid, toks
def usergrouper_combine(userid, tokenizations):
    wordset = set()
    for i,toks_str in enumerate(tokenizations):
        if i > 1e5: break
        toks = toks_str.split()
        for tok in toks:
            wordset.add(tok)
    yield userid, list(wordset)

def wc_map(userid, wordset):
    for w in wordset: yield w,1
def wc_sum(word, values):
    yield word, sum(values)

def final_filter(word, count):
    if count < 10: return
    yield word,count

class MyJob(MRJob):
    def steps(self):
        return [
            self.mr(mapper=usergrouper_map, reducer=usergrouper_combine),
            self.mr(mapper=wc_map, combiner=wc_sum, reducer=wc_sum),
            self.mr(mapper=final_filter),
            ]

if __name__ == '__main__':
    MyJob.run()

