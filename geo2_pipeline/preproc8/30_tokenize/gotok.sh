#!/bin/bash
# to be run on the mapper
set -eux
tar xf stuff.tar
java -XX:ParallelGCThreads=2 -Xmx200m -jar ark-tweet-nlp-0.3.1.jar --just-tokenize --input-field 3

