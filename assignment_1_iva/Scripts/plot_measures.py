#!/usr/bin/env python
import numpy
import sys
import matplotlib.pyplot as plt

score = sys.argv[1]
probs_file = sys.argv[2]

probs = open(probs_file).readlines()

probs = map(lambda x: float(x.strip('\n')), probs)

if score == 'Loglikelihood':
	min_ = round(min(probs), -3)
	max_ = round(max(probs), -3)

if score == 'Accuracy':
	min_ = min(probs)
	max_ = max(probs)

space = 0.3 * abs(max_-min_)
min_limit = min_ - space
max_limit = max_ + space

plt.figure()
plt.suptitle(score + ' per iteration')
plt.xlabel('Iteration')
plt.ylabel(score)
plt.ylim(min_limit, max_limit)
plt.plot(range(0, len(probs)), probs)
plt.savefig('Plot_' + score)


