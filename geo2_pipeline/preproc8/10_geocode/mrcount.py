from mrjob.job import MRJob
import re
import sys,json

class MyJob(MRJob):

    def mapper(self, _, line):
        date,geo,tweet = line.split('\t')
        geo = json.loads(geo)
        yield ((date[:7], geo.get('country')), 1)

    def combiner(self, key, counts):
        yield (key, sum(counts))

    def reducer(self, key, counts):
        yield (key, sum(counts))


if __name__ == '__main__':
    MyJob.run()

