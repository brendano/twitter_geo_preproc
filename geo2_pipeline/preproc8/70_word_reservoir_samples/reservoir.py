#!/usr/bin/env python
# For Hadoop Streaming
# must be only 1 reducer!!

## reduce step pass uses a weighted reservoir sampler to correct for variation in maptask split sizes
## WRS is from P.S. Efraimidis, P.G. Spirakis / Information Processing Letters 97 (2006) 181-185
## this seems to be a free version: http://utopia.duth.gr/~pefraimi/research/data/2007EncOfAlg.pdf
# unweighted reservoir sampler is knuth/vitter/???, see http://data-analytics-tools.blogspot.com/2009/09/reservoir-sampling-algorithm-in-perl.html
from __future__ import division


from collections import defaultdict
import random
import heapq

num_seen = defaultdict(int)

def add(L, N, x):
  """Call this many times.  L is a running sample, whose target size is N.
  We keep track of *i*, the number of items seen.  Return whether or not we added."""
  num_seen[make_it_hash(L)] += 1
  i = num_seen[make_it_hash(L)]
  if len(L) < N:
    L.append(x)
    return True
  if random.random() >= N/float(i):
    return False
  index = random.randint(0, len(L)-1)
  L[index] = x
  return True

def make_it_hash(L):
  "not really proper for mutable objects but we need a way to associate a list with an attribute"
  return id(L)


# from hose_util import *
# def mapper():
#   local_n = int(os.environ['LOCAL_N'])
#   sample = []
#   local_total = 0
#   for raw,tweet in iterate(raw=True):
#     add(sample, local_n, raw)
#     local_total += 1
# 
#   import hashlib
#   md5 = hashlib.md5()
#   for raw in sample: md5.update(raw)
#   subsample_code = md5.hexdigest()[:10]
# 
#   # local_total will eventually be used for reducestep weighting
# 
#   for raw in sample:
#     print "BLA\t%s:%d\t%s" % (subsample_code, local_total, raw)
# 
# def unweighted_reducer():
#   final_n = int(os.environ['FINAL_N'])
#   sample = []
#   for line in sys.stdin:
#     bla, partition_info, raw_tweet = line[:-1].split("\t")
#     add(sample, final_n, raw_tweet)
#   for raw in sample:
#     print raw
# 
# def weighted_reducer():
#   final_n = int(os.environ['FINAL_N'])
#   partition_sizes = {}
#   partition_samples=defaultdict(list)
#   M = 0
#   for i,line in enumerate(sys.stdin):
#     if i%1000 == 0:
#       print>>sys.stderr, "iter %d" % i
#       my_memory_usage()
#     bla, partition_info, raw_tweet = line[:-1].split("\t")
#     pname,psize = partition_info.split(":")
#     psize=int(psize)
#     partition_sizes[pname] = psize
#     partition_samples[pname].append(raw_tweet)
#     M += 1
#   
#   def yield_weighted_items():
#     for pname in partition_sizes.keys():
#       n = partition_sizes[pname]
#       N = len(partition_samples[pname])
#       #m = final_n
# 
#       weight = N/M / n
#       print>>sys.stderr,pname, N,n, M, weight
#       for item in partition_samples[pname]:
#         yield weight,item
# 
#   for w,x in heapq.nlargest(final_n, yield_weighted_items(), lambda (w,x): random.random() ** (1/w)):
#     print x
# 
# 
# 
# 
# if __name__=='__main__':
#   import os,sys
#   action = sys.argv[1]
#   assert action=='map' or action=='reduce'
#   assert 'FINAL_N' in os.environ
#   if 'LOCAL_N' not in os.environ:  os.environ['LOCAL_N'] = os.environ['FINAL_N']
#   if action=='map': mapper()
#   if action=='reduce': weighted_reducer()
