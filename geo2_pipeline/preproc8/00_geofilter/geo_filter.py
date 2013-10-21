#!/usr/bin/env python
import sys,os
sys.path.insert(0, os.path.join(os.path.dirname(__file__),'..'))
from hose_util import *

OneCoord = r'([-+]?\d{1,3}\.\d{3,})'
Separator= r', ?'
LatLong = re.compile(OneCoord + Separator + OneCoord, re.U)

VERBOSE = False

def reject(reason):
    global raw,tweet
    if not VERBOSE: return
    reject_key = "REJECT:" + reason
    output = "%s\t%s" % (reject_key, raw)
    print output

for raw,tweet in iterate(raw=True):
    lat = None
    lon = None
    loc_type = None

    geo = lookup(tweet, 'geo')
    if geo and geo['type'] == 'Point':
        lat,lon    = geo['coordinates']
        loc_type = 'OFFICIAL'
    else:
        loc = lookup(tweet, 'user.location').strip()
        if not loc:
            reject("NO USERLOC")
            continue
        m = LatLong.search(loc.encode('utf8'))
        if not m:
            reject("NO GEO REGEX ::: " + loc.encode('utf8').replace('\t',' ').replace('\n',' '))
            continue
        lat,lon = m.groups()
        loc_type = 'REGEX'

    try:
        lat=float(lat)
        lon=float(lon)
    except ValueError:
        # rejct("JUNK GEO\t" + json.dumps([lat,lon]))
        continue
    if (lat,lon)==(0,0) or lat < -90 or lat > 90 or lon < -180 or lon > 180:
        reject("JUNK GEO\t" + json.dumps([lat,lon]))
        continue

    record = {}
    record['lonlat'] = [lon,lat]
    record['loc_type'] = loc_type
    record['user_location'] = lookup(tweet, 'user.location')

    out = [
            tweet['created_at_iso'],
            json.dumps(record),
            raw
    ]
    if VERBOSE: out = ['ACCEPT'] + out

    print '\t'.join(out)
