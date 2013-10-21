set -eux
../maketar.sh
~/geo2/occ_env/bin/python useragg.py --verbose -r hadoop \
  --python-archive ../stuff.tar \
  --no-output  --jobconf mapred.reduce.tasks=20 \
  hdfs:///user/brendano/geocode.2009-201209.usa.msgfilter.tok \
  --output-dir hdfs:///user/brendano/useragg

  # hdfs:///user/brendano/geocode.2009-201209.usa.msgfilter.tok \
# yahoo-headnode:~/geo2/preproc8/40_useragg $ yahoo-headnode:~/geo2/preproc8/40_useragg $ ca^Ctoktweets.sample | ~/geo2/occ_env/bin/python useragg.py  --python-archive ../stuff.tar  > out


