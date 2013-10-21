import yajl,sys,os
import glob
import shapely.geometry
from shapely.ops import cascaded_union

for input in glob.glob("by_state/*.json"):
  base = os.path.basename(input).replace(".json","")
  print base

  d = yajl.load(open(input))
  polys = [shapely.geometry.shape(f['geometry']) for f in d['features'] ]
  union = cascaded_union(polys)
  print union.area
  with open("unions/" + base+".wkb", 'w') as out:
    out.write(union.wkb)


