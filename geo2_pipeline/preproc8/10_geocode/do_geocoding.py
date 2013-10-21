import sys,json
sys.path.insert(0,'geocode')
import geocode

for line in sys.stdin:
    parts = line.split('\t')
    geodict = json.loads(parts[1])
    geocode.geocode_world_country(geodict)
    geocode.geocode_us_county(geodict)
    parts[1] = json.dumps(geodict)
    sys.stdout.write('\t'.join(parts))
    # print>>sys.stderr,'.',

