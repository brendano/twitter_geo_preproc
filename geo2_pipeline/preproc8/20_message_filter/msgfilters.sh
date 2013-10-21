#!/bin/bash

# yahoo-headnode:~/geo2/preproc8/20_message_filter $ cat usafilter.out | PYTHONPATH=.. ~/geo2/occ_env/bin/python msgfilters.py --python-archive ../stuff.tar 

set -eux
../maketar.sh
export PYTHONPATH=..

~/geo2/occ_env/bin/python msgfilters.py --verbose -r hadoop \
  --python-archive ../stuff.tar \
  --no-output \
  hdfs:///user/brendano/geocode.2009-201209.usa  \
  --output-dir hdfs:///user/brendano/geocode.2009-201209.usa.msgfilter

