set -eux
(
hadoop jar /opt/hadoop/contrib/streaming/hadoop-streaming-0.20.203.0.jar  \
  -mapper geo_filter.py -file geo_filter.py -file ../hose_util.py         \
  -input 'share/allTwitter/tweets.2010*'       \
  -output geofilter.2010 \
  -reducer NONE
)
  # -input '/user/david/dbamman/allTwitter/tweets.2012-06-30T*'       \
