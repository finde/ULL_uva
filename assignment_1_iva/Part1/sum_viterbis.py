#!/usr/bin/env python
import numpy
import sys


probs_file = sys.argv[1]
output_file = sys.argv[2]

probs = open(probs_file).readlines()
output = open(output_file, 'a')

sum_probs=0

sum_probs=sum([float(prob.strip('\n')) for prob in probs])
#print sum_probs

output.write(str(sum_probs)+'\n')



