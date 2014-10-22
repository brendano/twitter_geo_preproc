A little Python geocoding library.  It can load a geojson database of
geographic features, then query a (lon,lat) coordinate for what feature it is
contained in.  It has been used successfully with library versions:

shapely 1.2.16 (https://pypi.python.org/pypi/Shapely)
rtree 0.7.0 (https://pypi.python.org/pypi/Rtree)
libgeos: geos-3.3.5 (c/c++ dependency for shapely)
libspatialindex: spatialindex-src-1.7.1 (c/c++ dependency for rtree)

or also this seems to work
shapely 1.4.3
rtree 0.8.0
libgeos 3.4.2  (debian package libgeos-dev)
libspatialindex 1.8.1 (debian package libspatialindex-dev)

Some sample geojson databases it has been used with are available at:
http://brenocon.com/geocode/

Example usage:
1. get the data and fix up paths in geocode.py
2. then the following should work.  Note that query_point() takes parameters as
   (longitude, latitude), though the (lat,lon) ordering is fairly conventional. 

$ python
>>> import geocode

>>> db=geocode.world_country()
geodb loading /home/brenocon/geocode/tm_world_borders-0.3.json

>>> db.query_point(-72.65,42.333333)
{u'type': u'Feature', u'properties': {u'SUBREGION': 21, u'NAME': u'United States', u'AREA': 915896, u'REGION': 19, u'LON': -98.606, u'ISO3': u'USA', u'ISO2': u'US', u'FIPS': u'US', u'UN': 840, u'LAT': 39.622, u'POP2005': 299846449}, 'shapely': <shapely.geometry.multipolygon.MultiPolygon object at 0x7f923c082950>}


>>> db=geocode.us_county()
geodb loading /home/brenocon/geocode/counties.tiger2010.json
[[ this takes a minute or so, and 1-2 GB RAM ]]

>>> db.query_point(-72.65,42.333333)
{u'type': u'Feature', u'properties': {u'NAME10': u'Hampshire', u'METDIVFP10': u'', u'CLASSFP10': u'H4', u'COUNTYNS10': u'00606934', u'AWATER10': 46500379.0, u'ALAND10': 1365585170.0, u'INTPTLAT10': u'+42.3394593', u'LSAD10': u'06', u'FUNCSTAT10': u'N', u'NAMELSAD10': u'Hampshire County', u'CSAFP10': u'', u'COUNTYFP10': u'015', u'CBSAFP10': u'44140', u'STATEFP10': u'25', u'MTFCC10': u'G4020', u'GEOID10': u'25015', u'INTPTLON10': u'-072.6636936'}, 'shapely': <shapely.geometry.polygon.Polygon object at 0x7f8a661ce190>}
 
