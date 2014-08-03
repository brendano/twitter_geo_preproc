A little Python geocoding library.  It can load a geojson database of
geographic features, then query a (lon,lat) coordinate for what feature it is
contained in.  It has been used successfully with library versions:

shapely 1.2.16 (https://pypi.python.org/pypi/Shapely)
rtree 0.7.0 (https://pypi.python.org/pypi/Rtree)

libgeos: geos-3.3.5 (c/c++ dependency for shapely)
libspatialindex: spatialindex-src-1.7.1 (c/c++ dependency for rtree)

Some sample geojson databases it has been used with are available at:
http://brenocon.com/geocode/
