__author__ = 'finde'


import numpy as np
from matplotlib import pyplot


rule = []
with open('rules.csv') as f:
    for n in f:
        rule.append(int(n))

    pyplot.plot(np.arange(0., 15000, 75), rule[1:])
    pyplot.title('Rule length overtime [flip]')
    pyplot.xlabel('Iteration')
    pyplot.ylabel('rule length')
    pyplot.savefig('mhasting_rule_length_set.png')