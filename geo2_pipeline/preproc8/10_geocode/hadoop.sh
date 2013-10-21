set -eux
../maketar.sh
function go() {
hadoop jar /opt/hadoop/contrib/streaming/hadoop-streaming-0.20.203.0.jar  \
  -mapper ./gogeo.sh -reducer NONE \
  -file gogeo.sh -file do_geocoding.py -file ../stuff.tar         \
  -input $1 -output $2
}
  # -input '/user/david/dbamman/allTwitter/tweets.2012-06-30T*'       \
  # -input 'geofilter.2009/part-00000'       \
  # -output geocode.test2

# go geofilter.2009  geocode.2009
# go geofilter.2010  geocode.2010
# go geofilter.2011  geocode.2011
# go geofilter.201201-201206 geocode.201201-201206
# go geofilter.201207-201209 geocode.201207-201209

go geofilter.* geocode.2009-201209
