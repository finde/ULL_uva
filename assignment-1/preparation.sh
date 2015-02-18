#!/bin/bash
treebank=$1
number_of_sentences=$2
n_iteration=$3
bitpar='../BitPar/src/bitpar'
f='output'

function preparation {
	treebank=$1
	number_of_sentences=$2
	f=$3

	echo "::Preparation::"
	echo " >> cleaning up the files"
	rm -rf $f
	mkdir $f

	echo " >> limiting treebanks to $number_of_sentences sentences"
	sed '/^$/d' $treebank > $f/treebank
	head -n $number_of_sentences $f/treebank > $f/new_treebank
	cat $f/new_treebank | sed 's/"//g' > $f/new_treebank_gold

	echo " >> extracting corpus from treebank"
	cat $f/new_treebank | sed 's/$/""\n/' | grep -E -o '"[^"]*"' | sed 's/"//g' > $f/_corpus
}