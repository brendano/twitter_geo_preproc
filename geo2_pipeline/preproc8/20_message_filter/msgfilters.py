from mrjob.job import MRJob
from mrjob.protocol import JSONValueProtocol, PickleProtocol, RawValueProtocol
import re,os,sys
# import simplejson as json
import json
from hose_util import lookup

LOWER_48 = """
AL	01	ALABAMA
AR	05	ARKANSAS
AZ	04	ARIZONA
CA	06	CALIFORNIA
CO	08	COLORADO
CT	09	CONNECTICUT
DC	11	DISTRICT OF COLUMBIA
DE	10	DELAWARE
FL	12	FLORIDA
GA	13	GEORGIA
IA	19	IOWA
ID	16	IDAHO
IL	17	ILLINOIS
IN	18	INDIANA
KS	20	KANSAS
KY	21	KENTUCKY
LA	22	LOUISIANA
MA	25	MASSACHUSETTS
MD	24	MARYLAND
ME	23	MAINE
MI	26	MICHIGAN
MN	27	MINNESOTA
MO	29	MISSOURI
MS	28	MISSISSIPPI
MT	30	MONTANA
NC	37	NORTH CAROLINA
ND	38	NORTH DAKOTA
NE	31	NEBRASKA
NH	33	NEW HAMPSHIRE
NJ	34	NEW JERSEY
NM	35	NEW MEXICO
NV	32	NEVADA
NY	36	NEW YORK
OH	39	OHIO
OK	40	OKLAHOMA
OR	41	OREGON
PA	42	PENNSYLVANIA
RI	44	RHODE ISLAND
SC	45	SOUTH CAROLINA
SD	46	SOUTH DAKOTA
TN	47	TENNESSEE
TX	48	TEXAS
UT	49	UTAH
VA	51	VIRGINIA
VT	50	VERMONT
WA	53	WASHINGTON
WI	55	WISCONSIN
WV	54	WEST VIRGINIA
WY	56	WYOMING
"""

LOWER_48 = LOWER_48.strip().split('\n')
LOWER_48 = [L.split()[0] for L in LOWER_48]
assert len(LOWER_48) == 49  ## lower48 and DC
LOWER_48 = set(LOWER_48)

def filter_lower48(geodict):
    """Returns boolean, whether is OK"""
    s = geodict.get('us_state')
    if not s: return False
    abb = s.get('abbrev')
    return abb in LOWER_48

def filter_tweet(tweet):
    """Returns:  (is_good_tweet, reason)"""

    source = lookup(tweet, 'source') or ""
    if "Buoy" in source:
        return False, "buoy"

    n_fol = lookup(tweet,'user.followers_count') or 0
    n_fri = lookup(tweet,'user.friends_count') or 0
    if not (n_fol < 1000 and n_fri < 1000): 
        return False, "too much follow"

    text = lookup(tweet, 'text')
    if not text or not text.strip():
        return False, "no text"
    if lookup(tweet, 'retweeted_status'):
        return False, "official RT"
    if re.search(r'\bRT\b', text):
        return False, "text RT"
    if re.search(r'\bhttps?:', text, re.I):
        return False, "url"

    return True, None


class FilterJob(MRJob):
    OUTPUT_PROTOCOL = RawValueProtocol
    def mapper(self, _, line):
        date,geo_s,tweet_s = line.split('\t')
        geo = json.loads(geo_s)
        if not filter_lower48(geo): 
            self.increment_counter('not in lower 48', geo.get('country','') + ' || ' +geo.get('us_state',{}).get('abbrev',''))
            # print geo
            return

        tweet = json.loads(tweet_s)
        keep, reason = filter_tweet(tweet)
        if not keep:
            # count the reason?
            self.increment_counter(reason,'')
            return
        self.increment_counter('keep','')
        yield None,line
        

if __name__=='__main__':
    FilterJob.run()

