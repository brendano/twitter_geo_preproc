from mrjob.job import MRJob
from mrjob.protocol import JSONValueProtocol, PickleProtocol, RawValueProtocol
# from hose_util import lookup
import re
import sys,json

class USAFilter(MRJob):
    OUTPUT_PROTOCOL = RawValueProtocol

    def mapper(self, _, line):
        line = line.rstrip('\n')
        date,geo,tweet = line.split('\t')
        geo = json.loads(geo)
        if geo.get('country')=='USA' or 'us_state' in geo:
            yield None, line

if __name__ == '__main__':
    USAFilter.run()

