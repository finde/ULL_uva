#!/usr/bin/python
import numpy
import sys


dependencies_file = sys.argv[1]
grammar_output_file = sys.argv[2]
lexicon_output_file = sys.argv[3]

dependencies = open(dependencies_file)
grammar_output = open(grammar_output_file, 'w')
lexicon_output = open(lexicon_output_file, 'w')


def L(H):
	return 'L_' + H + ' '

def L0(H):
	return 'L0_' + H + ' '

def L1(H):
	return 'L1_' + H + ' '



def R(H):
	return 'R_' + H + ' '

def R0(H):
	return 'R0_' + H + ' '

def R1(H):
	return 'R1_' + H + ' '



def Y(H):
	return 'Y_' + H + ' ' 

def l(H):
	return H + '_l '

def r(H):
	return H + '_r '




def root(H):
	root_rule = 'TOP ' + Y(H)
	YH_rule = Y(H) + L(H) + R(H)	
	
	LH_rule1 = L(H) + L0(H)
	LH_rule2 = L(H) + L1(H)
	
	L0H_rule = L0(H) + l(H)

	RH_rule1 = R(H) + R0(H)
	RH_rule2 = R(H) + R1(H)
	
	R0H_rule = R0(H) + r(H)


#	grammar_rules = [root_rule, YH_rule, LH_rule1, LH_rule2, L0H_rule, RH_rule1, RH_rule2, R0H_rule]
#	lexical_rules = [L0H_rule, R0H_rule]


	grammar_rules = [root_rule, YH_rule, LH_rule1, L0H_rule, RH_rule1, R0H_rule]
	lexical_rules = [L0H_rule, R0H_rule]

	return [grammar_rules, lexical_rules]


def left(H, A):
	L1H_rule = L1(H) + Y(A) + L(H)
	

#####
	YH_rule = Y(H) + L(H) + R(H)	
	
	LH_rule1 = L(H) + L0(H)
	LH_rule2 = L(H) + L1(H)
	
	L0H_rule = L0(H) + l(H)
#####

	grammar_rules = [L1H_rule]
	lexical_rules = []


#	grammar_rules = [L1H_rule, YH_rule, LH_rule1, LH_rule2, L0H_rule]
#	lexical_rules = [L0H_rule]

#	grammar_rules = [L1H_rule, LH_rule1, LH_rule2, L0H_rule]
#	lexical_rules = [L0H_rule]
	
#	grammar_rules = [L1H_rule, LH_rule2]


	return [grammar_rules, lexical_rules]


def right(H, A):
	R1H_rule = R1(H) + R(H) + Y(A)
	


#####
	YH_rule = Y(H) + L(H) + R(H)	
	
	RH_rule1 = R(H) + R0(H)
	RH_rule2 = R(H) + R1(H)
	
	R0H_rule = R0(H) + r(H)
#####

	grammar_rules = [R1H_rule]
	lexical_rules = []

#	grammar_rules = [R1H_rule, YH_rule, RH_rule1, RH_rule2, R0H_rule]
#	lexical_rules = [R0H_rule]

#	grammar_rules = [R1H_rule, RH_rule1, RH_rule2, R0H_rule]
#	lexical_rules = [R0H_rule]

#	grammar_rules = [R1H_rule, RH_rule2]


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










