# cat geocoded_tweets | python tweets2geojson.py > out.json
# ogr2ogr -f KML out.kml out.json
# ==> open out.kml in Google Earth

# 2009-01-04T21:24:03     {"loc_type": "REGEX", "lonlat": [-96.772514, 32.999172], "user_location": "iPhone: 32.999172,-96.772514", "country": "USA"}     {"favorited":false,"FROM_XML":true,"truncated":false,"text":"my sister wants to use twitter from her mobile phone in france, but the international number would cost her to use. Any good solutions?","created_at":"Sun Jan 04 21:24:03 +0000 2009","source":"<a href=\"http:\/\/iconfactory.com\/software\/twitterrific\">twitterrific<\/a>","in_reply_to_status_id":null,"in_reply_to_user_id":null,"id":1095775352,"user":{"description":"contains no MSG","url":"http:\/\/adam.speaksoutofturn.com","profile_image_url":"http:\/\/s3.amazonaws.com\/twitter_production\/profile_images\/57221924\/avatar_normal.jpg","name":"Adam French","followers_count":97,"protected":false,"location":"iPhone: 32.999172,-96.772514","id":5841912,"screen_name":"afcool83"}}

import sys,json
out = {}
out['type'] = 'FeatureCollection'
out['features'] = []
for line in sys.stdin:
    date, geo, tweet = line.split('\t')
    geo = json.loads(geo)
    tweet = json.loads(tweet)
    prop = {'date':date, 'text': tweet['text'], 
            'user.screen_name':tweet['user']['screen_name'],
            'user.location':tweet['user']['location'],
            'country': geo.get('country') }
    f = {'type':'Feature', 'properties':prop, 
            'geometry':{'type':'Point', 'coordinates': geo['lonlat']}
        }
    out['features'].append(f)


print json.dumps(out)

