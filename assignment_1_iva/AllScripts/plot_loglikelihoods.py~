#!/usr/bin/env python
import numpy
import sys
import matplotlib.pyplot as plt

probs_file = sys.argv[1]

probs = open(probs_file).readlines()

probs = map(lambda x: float(x.strip('\n')), probs)

min_limit = round(min(probs), -3) - 1000
max_limit = round(max(probs), -3) + 1000

plt.figure()
plt.suptitle('Loglikelihood per iteration')
plt.xlabel('Iteration')
plt.ylabel('Loglikelihood')
plt.ylim(min_limit, max_limit)
plt.plot(range(0, len(probs)), probs)
plt.savefig('Plot_Loglikelihood')


