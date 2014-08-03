import state_codes
import geodb

# Copies of these here: http://brenocon.com/geocode/
paths = {
'world_country': '/home/brendano/geo/geodata/world.json',
'us_county':     '/home/brendano/geo/geodata/counties.tiger2010.json',
}

### Lazy loading of geo databases

_dbs = {}

def us_county():
    global _dbs
    if not _dbs.get('us_county'):
        _dbs['us_county'] = geodb.GeoDB.load_geojson_files([paths['us_county']])
    return _dbs['us_county']
        
def world_country():
    global _dbs
    if not _dbs.get('world_country'):
        _dbs['world_country'] = geodb.GeoDB.load_geojson_files([paths['world_country']])
    return _dbs['world_country']

### Geocode into a "geo info" dict

def geocode_us_county(geodict):
    lon,lat = geodict['lonlat']
    f = us_county().query_point(lon,lat)
    if f:
        geodict['us_state'] = {}
        geodict['us_state']['fp10'] = f['properties']['STATEFP10']
        geodict['us_state']['abbrev'] = state_codes.fips2postal.get(geodict['us_state']['fp10'])
        geodict['us_county'] = {}
        geodict['us_county']['fp10'] = f['properties']['COUNTYFP10']
        geodict['us_county']['namelsad'] = f['properties']['NAMELSAD10']
        geodict['us_county']['geoid10']  = f['properties']['GEOID10']

def geocode_world_country(geodict):
    lon,lat = geodict['lonlat']
    f = world_country().query_point(lon,lat)
    if f:
        geodict['country'] = f['properties']['ISO3']
        # geodict['country'] = {'iso3':f['properties']['ISO3']}

