class Kahan:
    """http://en.wikipedia.org/wiki/Kahan_summation_algorithm"""
    def __init__(self):
        self.sum = 0
        self.c = 0
    def add(self, value):
        self.y = value - self.c
        t = self.sum + self.y
        self.c = (t-self.sum) - self.y
        self.sum = t

