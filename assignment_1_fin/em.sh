#!/bin/bash
function em {
	f=$1
	n_iteration=$2
	DIR=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )

	echo "::EM::"
	for i in `seq 1 $n_iteration`;
	do
		echo ' >> Iteration-'$i

#		echo " - Do a single pass of io with bitpar"
		$bitpar -s TOP $f/em.gram $f/em.lex $f/_corpus -em $f/em

		# # remove lines with 0 counts
		less $f/em.gram | grep -v '0\.00' > $f/em.grammar
		less $f/em.lex | grep -v '0\.000*' | awk '{print $1"\t"$2" "$3 }' > $f/em.lexicon

		rm -f $f/em.gram && rm -f $f/em.lex && mv $f/em.grammar $f/em.gram && mv $f/em.lexicon $f/em.lex && $bitpar -q -s TOP -b 1 $f/em.gram $f/em.lex $f/_corpus > $f/_forest
		sed -i '' 's/\\//g' $f/_forest

#		echo " -  evaluation"
		$bitpar -q -vp -s TOP $f/em.gram $f/em.lex $f/_corpus | grep -E -o '^[{]*\(TOP=\#i\[P=[0-9]+\.[0-9]*[-e]*[0-9]*\]' | grep -E -o '[0-9]+\.[0-9]*[-e]*[0-9]*' > $f/_output

		# sum to get log-likelihood from file $output
		likelihood=$(python $DIR/sum_log_probabilities.py $f/_output | sed 's/.*\[\(.*\)\].*/\1/' | tr -d ' ')

#		echo " - running evalC"
		recall_precision_fscore=$(java -jar $DIR/../evalC/evalC.jar $f/new_treebank_gold $f/_forest $f/_eval_$i | sed 's/.*\[\(.*\)\].*/\1/' | tr -d ' ' | tr ',' ' ')
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
		echo $i","$likelihood","$recall","$precision","$fscore >> $f/results.csv
	done
}