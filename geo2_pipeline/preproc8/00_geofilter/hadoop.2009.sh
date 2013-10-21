set -eux
(
hadoop jar /opt/hadoop/contrib/streaming/hadoop-streaming-0.20.203.0.jar  \
  -mapper geo_filter.py -file geo_filter.py -file ../hose_util.py         \
  -input 'share/allTwitter/tweets.2009*'       \
  -output geofilter.2009 \
  -reducer NONE
)
  # -input 'share/allTwitter/tweets.2012-0[1-6]*'       \
  # -output geofilter.201201-201206 \
  # -input '/user/david/dbamman/allTwitter/tweets.2012-06-30T*'       \
