import json,sys,cgi

d = json.loads(sys.stdin.read())

wordlist_file = "/home/brendano/geo/GeoTM/geo2/model/allwords.sorted.md5.txt"
allwords = [L.split()[-1] for L in open(wordlist_file)]


newnums = {w:i for i,w in enumerate(allwords)}
print "TOC"
print "<ol>"
for w in allwords:
    if not d[w]: continue
    print "<li><a href='#%d'>%s</a>" % (newnums[w], cgi.escape(w))
print "</ol>"

print "<hr>"

for w in allwords:
    samples = d[w]
    if not samples: continue
    # print
    # print "===", w
    print "<a name='%d'>" % newnums[w]

    print "<h2>", cgi.escape(w), "</h2>"
    print "</a>"
    print "<ol>"
    for samp in samples:
        # print samp
        print "<li>"
        tokens = samp.split()
        for tok in tokens:
            tokhtml = cgi.escape(tok)
            if tok==w:
                tokhtml = "<b>" + tokhtml + "</b>"
            print tokhtml
        # print "<li>", cgi.escape(samp)
    print "</ol>"

