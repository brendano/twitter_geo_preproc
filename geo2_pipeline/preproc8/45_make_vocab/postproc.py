import sys,json
wc = []
for line in sys.stdin:
    word, count = line.split('\t')
    count = int(count)
    word = json.loads(word)
    wc.append( (word,count) )

wc.sort(key=lambda (w,c): (-c, w))
for w,c in wc:
    print "{}\t{}".format(w,c)

