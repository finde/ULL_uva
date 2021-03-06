#!/usr/bin/python
import numpy
import sys


dependencies_file = sys.argv[1]
grammar_output_file = sys.argv[2]
lexicon_output_file = sys.argv[3]

dependencies = open(dependencies_file)
grammar_output = open(grammar_output_file, 'w')
lexicon_output = open(lexicon_output_file, 'w')


def L(u):
	return 'L_' + u + ' '


def R(u):
	#return u + '_R' + ' '
	return 'R_' + u + ' '

def X(u):
	return 'X_' + u + ' ' 

def l(u):
	return u + '_l '

def r(u):
	return u + '_r '

def root(u):
	root_rule = 'TOP ' + X(u)
	rewrite_rule = X(u) + L(u) + R(u)	

	left_terminal_rule = L(u) + l(u)
	right_terminal_rule = R(u) + r(u)

	grammar_rules = [root_rule, rewrite_rule, left_terminal_rule, right_terminal_rule]
	lexical_rules = [left_terminal_rule, right_terminal_rule]

	return [grammar_rules, lexical_rules]


def left(u, v):
	left_rule = L(u) + X(v) + L(u)
	
#	left_rule_u = L(v) + l(v)
#	right_rule_u = R(u) + r(u)

#	left_rule_v = L(v) + l(v)
#	right_rule_v = R(v) + r(v)
	

#	grammar_rules = [left_rule, left_rule_u, right_rule_u, left_rule_v, right_rule_v]
#	lexical_rules = [left_rule_u, right_rule_u, left_rule_v, right_rule_v]

	grammar_rules = [left_rule]
	lexical_rules = []

	return [grammar_rules, lexical_rules]


def right(u, v):
	right_rule = R(u) + R(u) + X(v)
	
#	left_rule_u = L(v) + l(v)
#	right_rule_u = R(u) + r(u)

#	left_rule_v = L(v) + l(v)
#	right_rule_v = R(v) + r(v)
	

#	grammar_rules = [right_rule, left_rule_u, right_rule_u, left_rule_v, right_rule_v]
#	lexical_rules = [left_rule_u, right_rule_u, left_rule_v, right_rule_v]

	grammar_rules = [right_rule]
	lexical_rules = []


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











