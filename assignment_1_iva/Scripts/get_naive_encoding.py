#!/usr/bin/python
import numpy
import sys


dependencies_file = sys.argv[1]
grammar_output_file = sys.argv[2]
lexicon_output_file = sys.argv[3]

dependencies = open(dependencies_file)
grammar_output = open(grammar_output_file, 'w')
lexicon_output = open(lexicon_output_file, 'w')


def X(u):
	return 'X_' + u + ' '



def root(u):
	root_rule = 'TOP ' + X(u)
	terminal_rule = X(u) + u

	grammar_rules = [root_rule, terminal_rule]
	lexical_rules = [terminal_rule]

	return [grammar_rules, lexical_rules]


def left(u, v):
	left_rule = X(u) + X(v) + X(u)
	
	terminal_rule_u = X(u) + u
	terminal_rule_v = X(v) + v

	grammar_rules = [left_rule, terminal_rule_u, terminal_rule_v]
	lexical_rules = [terminal_rule_u, terminal_rule_v]

	return [grammar_rules, lexical_rules]


def right(u, v):
	right_rule = X(u) + X(u) + X(v)

	terminal_rule_u = X(u) + u
	terminal_rule_v = X(v) + v
	
	grammar_rules = [right_rule, terminal_rule_u, terminal_rule_v]
	lexical_rules = [terminal_rule_u, terminal_rule_v]

	return [grammar_rules, lexical_rules]


for dep_rule in dependencies:
	splitted = dep_rule.strip('\n').split()
	if splitted[0] == 'ROOT':
		[grammar_rules, lexical_rules] = root(splitted[1])
	else:
		if splitted[2] == 'left':
			[grammar_rules, lexical_rules] = left(splitted[0], splitted[1])

		else:
			[grammar_rules, lexical_rules] = right(splitted[0], splitted[1])
			
	
	for each in grammar_rules:
		grammar_output.write(each+'\n')
	for each in lexical_rules:
		lexicon_output.write(each+'\n')











