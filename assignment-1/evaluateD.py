#Compute the average accuracy of a file with dependency skeletons.
#Usage: python test gold

import sys

def main():
	ftest = open(sys.argv[1])
	fgold = open(sys.argv[2])
	line_test = ftest.readline()
	line_gold = fgold.readline()
	nr_of_sentences = 0
	A = 0
	while line_test != '':
		nr_of_sentences += 1
		score = 0
		test = line_test.split()
		gold = line_gold.split()
		assert len(test) == len(gold), "gold sentence %i and input sentence %i do not have the same length" % (nr_of_sentences, nr_of_sentences)
		for i in range(len(test)):
			if test[i] == gold[i]:
				score +=1
		accuracy = float(score)/len(test)
		A += accuracy
		line_test, line_gold = ftest.readline(), fgold.readline()
	print "\nnr of sentences: %i" % nr_of_sentences
	print "average accuracy per sentence: %f" % (A/float(nr_of_sentences))
	return A/float(nr_of_sentences)


if __name__ == '__main__':
	main()
