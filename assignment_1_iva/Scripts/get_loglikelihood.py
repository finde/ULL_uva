#!/usr/bin/env python
import math
import sys
 
prob_file = sys.argv[1]
output_file = sys.argv[2]

probs = open(prob_file, 'r')
output = open(output_file, 'a')
 
log_prob_total = sum([math.log(float(line)) for line in probs])

output.write(str(log_prob_total)+'\n') 

probs.close()
output.close()

print "The sum of the log of all probabilities in input file is:", log_prob_total
