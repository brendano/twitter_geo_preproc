import sys,re
import json
import reservoir
wordlist_file = "/home/brendano/geo/GeoTM/geo2/model/allwords.sorted.md5.txt"

N = 20

allwords = [L.split()[-1] for L in open(wordlist_file)]
word_samples = {w:[] for w in allwords}

# def disjunction(wordlist):
#     regex = r' (' + '|'.join(re.escape(w) for w in wordlist) + r') '
#     regex = re.compile(regex)
#     return regex
# 
# K = 1000
# regexes = [disjunction(allwords[i:(i+K)]) for i in range(0, len(allwords), K)]


for line in sys.stdin:
    text = line.split('\t')[-1].strip()
    text = ' ' + text + ' '
    # if not any(r.search(text) for r in regexes): continue
    for w in text.split():
        if w in word_samples:
            reservoir.add(word_samples[w], N, text.strip())

print json.dumps(word_samples)
