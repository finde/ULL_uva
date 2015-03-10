#!/usr/bin/env python
import math
import sys
 
prob_file = sys.argv[1]

probs = open(prob_file, 'r')

log_prob_total = sum([float(line) for line in probs])

probs.close()

print "The sum of the log of all probabilities in input file is:[", log_prob_total,"]"
