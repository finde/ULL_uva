#!/usr/bin/env python
import numpy
import sys


corpus = sys.argv[1]

corpus_temp = corpus + '_temp'
corpus_current = corpus + '_current'

lines = open(corpus_temp).readlines()
current = open(corpus_current, 'w')

for i, line in enumerate(lines[:]):
	if line=='\n':
		del lines[0]
		break	
	current.write(line)
	del lines[0]

open(corpus_temp, 'w').writelines(lines)



