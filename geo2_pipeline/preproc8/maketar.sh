cd $(dirname $0)
tar cf stuff.tar *.py
tar rf stuff.tar nlp
tar rf stuff.tar ../geocode/*.py
cp ~/ark-tweet-nlp-0.3.1/ark-tweet-nlp-0.3.1.jar . && tar rf stuff.tar ark-tweet-nlp-0.3.1.jar
cp ~/profile . && tar rf stuff.tar profile && rm profile
