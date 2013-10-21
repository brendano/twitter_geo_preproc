#!/bin/bash
~/geo2/occ_env/bin/python usafilter.py --verbose -r hadoop \
  hdfs:///user/brendano/geocode.2009-201209  \
  --no-output \
  --output-dir hdfs:///user/brendano/geocode.2009-201209.usa
