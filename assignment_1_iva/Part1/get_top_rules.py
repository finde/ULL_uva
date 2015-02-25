#!/usr/bin/python
import numpy
import sys


grammar = sys.argv[1]
top = int(sys.argv[2])

rules = open(grammar)
top_file = open('top_rules', 'w')
rules_dict = {}
#rules_list=list()
#rules_prob=list()
#i = 0



for rule in rules:
	splitted = rule.strip('\n').split('\t')
	if len(splitted) > 1:
		rules_dict[splitted[1]] = float(splitted[0])
	else:
		splitted = splitted[0].split()
		rule = ' '.join(splitted[1:])
		prob = float(splitted[0])
		rules_dict[rule] = prob 

it = iter(sorted(rules_dict.items(), key=lambda(key, value): value, reverse=True))

for i in range(0, top):
	next = it.next()
	print next
	top_file.write(str(next)+'\n')


