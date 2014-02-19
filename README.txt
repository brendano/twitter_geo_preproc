geo_filter.py is an example script for filtering to geocoded tweets from
Twitter's Streaming API.

One thing is, this script uses a regex that gets locations for substantially more 
tweets than Twitter's own official geo metadata, via lat/long coordinates in
the user.location field.  In the far-enough past, these unofficial data were
the only source of geolocation metadata.

hose_util.py has a convenience function to safely iterate through tweets from a
stream.

twokenize.py, emoticons.py is a tokenizer.

geo2_pipeline/ is a processing pipeline that also includes U.S. county geocoding.

--Brendan O'Connor (http://brenocon.com)
