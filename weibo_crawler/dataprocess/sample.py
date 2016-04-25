import pylab
import random

SAMPLE_SIZE = 100
random.seed()
real_rand_vars = []
real_rand_vars = [random.random() for val in xrange(SAMPLE_SIZE)]
pylab.hist(real_rand_vars,10)

pylab.xlabel("Number range")
pylab.ylabel("Count")

pylab.show()
