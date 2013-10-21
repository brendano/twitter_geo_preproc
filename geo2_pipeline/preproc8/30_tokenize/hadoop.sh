# -file (reverse-i-search)`twokenize': cat geocode.sample | ~/ark-tweet-nlp-0.3.1/twokenize.sh --input-field 3 | cut -f1 > tok.java
# java -XX:ParallelGCThreads=2 -Xmx100m -jar $(dirname $0)/ark-tweet-nlp-0.3.1.jar --just-tokenize "$@"

set -eux
hadoop jar /opt/hadoop/contrib/streaming/hadoop-streaming-0.20.203.0.jar  \
  -mapper ./gotok.sh  -file gotok.sh \
  -file ../stuff.tar \
  -reducer NONE \
  -input geocode.2009-201209.usa.msgfilter \
  -output geocode.2009-201209.usa.msgfilter.tok 

  # -input geocode.2009-201209.usa \
  # -output geocode.2009-201209.usa.tok 

  # -input geocode.test2 \
  # -output tok.test

  # -file $HOME/ark-tweet-nlp-0.3.1/ark-tweet-nlp-0.3.1.jar \
  # -mapper "tar xf stuff.tar; java -XX:ParallelGCThreads=2 -Xmx200m -jar ark-tweet-nlp-0.3.1.jar --just-tokenize --input-field 3" \
