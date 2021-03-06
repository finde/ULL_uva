#!/usr/bin/env python
import numpy
import sys
import matplotlib.pyplot as plt

scores_file = sys.argv[1]

lines = open(scores_file).readlines()

recalls = []
precisions = []
f_scores = []

for each in lines:
	splitted = each.strip('\n').split(': ')
	scores = splitted[1].strip('[').strip(']').split(',')
	scores = map(lambda x: float(x)/100, scores)
	recalls.append(scores[0])
	precisions.append(scores[1])
	f_scores.append(scores[2])

iterations = range(0, len(recalls)) 

min_limit = min(min(recalls), min(precisions), min(f_scores)) - 0.05
max_limit = max(max(recalls), max(precisions), max(f_scores)) + 0.05


plt.figure()
plt.suptitle('Scores per iteration')
plt.xlabel('Iteration')
plt.ylabel('Parse Accuracy')
plt.ylim(min_limit, max_limit)
plt.plot(iterations, recalls, label='Recall')
plt.plot(iterations, precisions, label='Precision')
plt.plot(iterations, f_scores, label='F Score')
plt.legend()
plt.savefig('Plot_scores')

