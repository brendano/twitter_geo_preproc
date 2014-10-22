# Loading all ZCTAs takes 9.5 GB RAM
# Loading all counties takes 1.3 GB RAM

import json
import glob,os,sys,re,itertools
import shapely.wkb
from shapely.geometry import Point
import rtree

class GeoDB:
    """
    geofeats: list of GeoJSON features (with 'shapely' instead of 'geometry')
    """
    def __init__(self):
        self.geofeats = []
        self.index = rtree.index.Index()
    def add(self, geofeat):
        new_featid = len(self.geofeats)
        self.index.insert(new_featid, geofeat['shapely'].bounds)
        self.geofeats.append(geofeat)
    def query_point(self, x,y):
        results = self.index.intersection((x,y,x,y))
        results = (self.geofeats[id] for id in results)
        results = (f for f in results if f['shapely'].contains(Point(x,y)))
        results = list(results)
        if len(results)==0:
            return None
        if len(results) > 1:
            print>>sys.stderr, "warning %d results on geodb lookup" % len(results)
        return results[0]

    @staticmethod
    def load_geojson_files(filenames):
        """Use all features from all files"""
        db = GeoDB()
        for filename in filenames:
            print>>sys.stderr, "geodb loading", filename
            feats = read_geojson_features(filename)
            for feat in feats:
                db.add(feat)
        return db

class LazyHierGeoDB:
    """
    Store a higher level of the hierarchy in memory. Lazily load subparts as necessary.
    """
    def __init__(self):
        pass

def read_geojson_features(filename):
    """
    Load  GeoJSON features from a datafile; convert "geometry" field to a
    "shapely" field: substantially more memory-efficient.
    """
    # ogr2ogr has a ?bug that the JSON file isn't utf8. not sure what's going on.
    json_data = open(filename).read().decode('utf8', 'replace')
    json_data = json.loads(json_data)
    assert json_data['type'] == 'FeatureCollection'
    for feat in json_data['features']:
        shape = shapely.geometry.shape(feat['geometry'])
        feat['shapely'] = shape
        del feat['geometry']
    return json_data['features']

