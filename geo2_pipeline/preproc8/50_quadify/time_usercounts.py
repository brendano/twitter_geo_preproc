from collections import defaultdict
import sys
time_to_users = defaultdict(set)

alltimes = set()

for line in sys.stdin:
    time,region,user,word,wc = line.split()
    time=int(time)
    time_to_users[time].add(user)
    alltimes.add(time)

for time in sorted(alltimes):
    print time, len(time_to_users[time])



