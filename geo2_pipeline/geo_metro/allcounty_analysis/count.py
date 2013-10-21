import ujson as json
from collections import defaultdict
import sys

countylists = {
        'msa_whitelist': set(open("msa_counties_kept.fips").read().split()),
        'msa_blacklist': set(open("msa_counties_notused.fips").read().split()),
        }

assert not countylists['msa_whitelist'] & countylists['msa_blacklist']

counts = defaultdict(int)
for line in sys.stdin:
    geo = json.loads(line)
    countyfips = geo['us_county']['geoid10']
    if countyfips in countylists['msa_whitelist']:
        counts['msa_whitelist'] += 1
    elif countyfips in countylists['msa_blacklist']:
        counts['msa_blacklist'] += 1
    else:
        counts['not_in_any_msa'] += 1

print dict(counts)

