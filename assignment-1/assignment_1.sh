#!/bin/bash
set -e

treebank=$1
number_of_sentences=$2
n_iteration=$3
bitpar='../BitPar/src/bitpar'
f='output'

function preparation {
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

function grammar_extraction_pcfg {
	echo "::Extracting grammars with PCFG::"
	echo " >> running PCFG extractor .."
	java -jar ../PCFG_extractor.jar $f/new_treebank $f/_treebanks.grammar

	echo " >> Rearrange information such that it becomes suitable for Bitpar"
	less $f/_treebanks.grammar | sed 's/%/%%/g' | awk '{printf ($NF " "); for (i=1; i<NF; i++) printf ($i " "); printf ("\n");}' > $f/em.gram
	less $f/em.gram | grep -E '"[^"]+"' | sed 's/\"//g' | awk '{print($3"\t"$2"\t"$1)}' > $f/em.lex
	sed -i '' 's/"//g' $f/em.gram
}

function em {
	echo "::EM::"
	for i in `seq 1 $n_iteration`;
	do
		echo ' >> Iteration-'$i

#		echo " - Do a single pass of io with bitpar"
		$bitpar -q -s TOP $f/em.gram $f/em.lex $f/_corpus -em $f/em

		# # remove lines with 0 counts
		less $f/em.gram | grep -v '0\.00' > $f/em.grammar
		less $f/em.lex | grep -v '0\.000*' | awk '{print $1"\t"$2" "$3 }' > $f/em.lexicon

		rm -f $f/em.gram && rm -f $f/em.lex
		mv $f/em.grammar $f/em.gram
		mv $f/em.lexicon $f/em.lex

#		echo " - get the forest of PCFGs"
		$bitpar -q -s TOP -b 1 $f/em.gram $f/em.lex $f/_corpus > $f/_forest
		sed -i '' 's/\\//g' $f/_forest

#		echo " -  evaluation"
		$bitpar -q -ip -s TOP $f/em.gram $f/em.lex $f/_corpus> $f/_forest_proba
		cat $f/_forest_proba | grep -E -o '^[{]*\(TOP=\#i\[P=[0-9]+\.[0-9]*[-e]*[0-9]*\]' | grep -E -o '[0-9]+\.[0-9]*[-e]*[0-9]*' > $f/_output_$i

		# sum to get log-likelihood from file $output
		likelihood=$(python ../sum_log_probabilities.py $f/_output_$i | sed 's/.*\[\(.*\)\].*/\1/' | tr -d ' ')

#		echo " - running evalC"
		recall_precision_fscore=$(java -jar ../evalC/evalC.jar $f/new_treebank_gold $f/_forest $f/_eval_$i | sed 's/.*\[\(.*\)\].*/\1/' | tr -d ' ' | tr ',' ' ')
		recall=$(awk '{ print $1 }' <<< "$recall_precision_fscore")
		precision=$(awk '{ print $2 }' <<< "$recall_precision_fscore")
		fscore=$(awk '{ print $3 }' <<< "$recall_precision_fscore")

		echo " ->> likelihood:  "$likelihood
		echo " ->> recall:      "$recall
		echo " ->> precision:   "$precision
		echo " ->> fscore:      "$fscore

		if [ $i -eq 1 ] ;
		then
			echo "iteration,likelihood,recall,precision,fscore" >> $f/results.csv
		fi
		echo "#"$i","$likelihood","$recall","$precision","$fscore >> $f/results.csv
	done
}

########### MAIN FUNCTION  ################
preparation
grammar_extraction_pcfg
em