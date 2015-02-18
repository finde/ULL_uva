import sys
import math

prob_file = sys.argv[1]
f = open(prob_file, 'r')

log_prob_total = 0.0

for line in f:
    prob = float(line)
    logprob = math.log(float(line))
    log_prob_total += logprob

f.close()

print "The sum of the log of all probabilities in input file is: [", log_prob_total, "]"
