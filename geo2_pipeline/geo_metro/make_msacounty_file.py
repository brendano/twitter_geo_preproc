# python make_msacounty_file.py > msa_counties.tsv

import re
from collections import defaultdict
import xlrd

## Ranking of MSA's by population, used for numberization
# msanames_by_pop = [L.strip().split('\t')[-1] for L in open("lat_long_pop_msa.tsv")]
msas = [L.strip().split('\t')[:2] for L in open("new_wikipedia_list.tsv")]
assert msas[0][0] == 'Rank'
msas = msas[1:]
# msas = msas[:200]
msaname_to_rank = {re.sub(r' MSA$',"",name).strip(): int(rank) for rank,name in msas}

## County <-> MSA mapping, from
book = xlrd.open_workbook("orig2009/CountiesWithMSACodes_List3.xls")
sheet = book.sheets()[0]

header_row = 3
fieldnames = [sheet.cell(header_row, j).value for j in range(sheet.ncols)]
rowdicts = [{fieldnames[j]: sheet.cell(i,j).value for j in range(sheet.ncols)}
                for i in range(header_row+1, sheet.nrows) ]


county_msa_records = []
for d in rowdicts:
    # d['CBSA Title'] = d['CBSA Title'].replace("--","-")
    if d['Level of CBSA'] != 'Metropolitan Statistical Area':
        # print "Not a Metro SA |||", d['CBSA Title']
        continue
    if d['CBSA Title'] not in msaname_to_rank:
        # print "Not in MSA filter list |||", d['CBSA Title']
        continue
    else:
        # print "Using ||| ", d['CBSA Title']
        county_msa_records.append(d)

msa2counties = defaultdict(list)
for d in county_msa_records:
    msa2counties[d['CBSA Title']].append(d['FIPS'])

print '\t'.join(['rank','msaname','county_fips'])
for msaname,rank in sorted(msaname_to_rank.items(), key=lambda (n,r): r):
    print '\t'.join([str(rank), msaname, ','.join(msa2counties[msaname])])
