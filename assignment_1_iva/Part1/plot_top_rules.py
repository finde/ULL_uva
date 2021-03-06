#!/usr/bin/env python
import numpy
import sys
import matplotlib.pyplot as plt
import re

rules_file = sys.argv[1]

rules_lines = open(rules_file).readlines()

rules_dict = {}
iteration = -1

for each in rules_lines:
	if re.match('ITERATION', each):
		iteration+=1
		rules_dict[iteration] = {}
	else:
		splitted = each.strip('\n').strip('(').strip(')').split(',')
		rules_dict[iteration][splitted[0]] = float(splitted[1])


rules_list = [each.keys() for each in rules_dict.values()]
intersection = set.intersection(*(map(set, rules_list)))

probabilities = {rule: [] for rule in intersection}

for it in range(0, iteration+1):
	for rule in intersection:
		probabilities[rule].append(rules_dict[it][rule])

plt.figure()
plt.suptitle('Rule probabilities per iteration')
plt.xlabel('Iteration')
plt.ylabel('Rule probability')

for rule in intersection:
	splitted = rule.strip("'").split()
	head = splitted[0]
	rewrite = ' '.join(splitted[1:])
	plt.plot(range(0, iteration+1), probabilities[rule], label=head+r'$\rightarrow$'+rewrite)

plt.legend()
plt.savefig('Plot_rules')

