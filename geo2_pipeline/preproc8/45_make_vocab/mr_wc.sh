set -eux
~/geo2/occ_env/bin/python  mr_wc.py -r hadoop hdfs:///user/brendano/smalltweets2 --jobconf mapred.reduce.tasks=200 --no-output --output-dir hdfs:///user/brendano/smalltweets2.word_usercount2

