#!/bin/bash
set -eux

# cat ../40_useragg/toktweets.sample | py smallify.py --python-archive ../stuff.tar  > out

~/geo2/occ_env/bin/python smallify.py --verbose -r hadoop \
  --python-archive ../stuff.tar \
  --jobconf mapred.reduce.tasks=50 --no-output \
  --no-output \
                hdfs:///user/brendano/geocode.2009-201209.usa.msgfilter.tok \
  --output-dir  hdfs:///user/brendano/smalltweets2
