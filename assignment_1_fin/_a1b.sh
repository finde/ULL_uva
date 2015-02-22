#!/bin/bash
set -e

treebank=$1
number_of_sentences=$2
n_iteration=$3
DIR=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )
bitpar=$DIR'/../BitPar/src/bitpar'
f=$4

#. $DIR/preparation.sh
#. $DIR/grammar_extraction_pcfg.sh
#. $DIR/em.sh
. $DIR/dep2pcfg.sh

rm -rf $f
mkdir $f

sentence_file=$DIR/$f/'_seq.txt'
sentences=$DIR/$f/'_sens_10tag.txt'
sentences_double=$DIR/$f/'_sens_10tag_double.txt'
all_dependencies=$DIR/$f/'_all_dependencies.txt'
headden_transform=$DIR/$f/'_headden_transform.txt'

lexicon=$DIR/$f/'_lexicon.txt'
corpus=$DIR/$f/'_corpus.txt'
grammar=$DIR/$f/'_grammar.txt'
em=$DIR/$f/'_em'

########### MAIN FUNCTION  ################

###############################################################################
# Extract POS-tag sequences from a treebank $treebank and write them to a file called $output
cat $treebank | sed '/^$/d' | sed  -e 's/(/((/g;s/([^"]*(//g;s/ "[^)]*//g;s/)//g' > $sentence_file

# using words
#cat $treebank | sed '/^$/d' | sed -e 's/([^"]* "//g;s/"[^ ]*//g' > $sentence_file

#################################################################################
## Filtering out sentences with up to 10 tags
cat $sentence_file | awk '{if (NF<11) print}' | head -n $number_of_sentences > $sentences

################################################################################
# Extract all dependencies from a file with sentences of words or POS tags

# extract all possible dependencies
cat $sentences |  awk '{for (i=1;i<=NF;i++) {print "ROOT",$i, "right"; for (j=i+1;j<=NF;j++) {print $i,$j, "right"; print $j,$i, "left"}}}' > $all_dependencies

### sort, count and sort again
cat $all_dependencies | sort | uniq -c | sort -g -r -k 1 | sed 's/ *[0-9]* //' | dmv | sort > $headden_transform

#cat $headden_transform

##################################################################################
# Annotate dependency parses encoded as CF-trees with Headden's transform with heads
cat $headden_transform | uniq -c | sed 's/^ *//' > $em.gram
cat $em.gram | grep -E '_l|_r' | awk '{printf("%s\t%s\t%s\n",$3,$2,$1)}' > $em.lex
sed -i '' '/_[lr]$/d' $em.gram
#sed -i '' 's/[0-9]* /1/' $em.gram

# convert sentences to double -> split head
cat $sentences | awk '{for (i=1;i<=NF;i++){printf("%s_l\n%s_r\n",$i,$i)}printf("\n")}' > $sentences_double

    echo "::EM::"
	for i in `seq 1 $n_iteration`;
	do
	    echo '======='
		echo ' >> Iteration-'$i
        echo '======='

        $bitpar -q -s S $em.gram $em.lex $sentences_double -em $em

        less $em.gram | grep -v '0\.00' > $em.grammar
        less $em.lex | grep -v '0\.000*' | awk '{print $1"\t"$2" "$3 }' > $em.lexicon

        rm -f $em.gram && rm -f $em.lex && mv $em.grammar $em.gram && mv $em.lexicon $em.lex && $bitpar -q -s S -b 1 $em.gram $em.lex $sentences_double | sed 's/\\//g' > $f/_forest.txt

        #echo "evaluation"
        $bitpar  -q -ip -s S $em.gram $em.lex $sentences_double > $f/_forest_proba.txt
        cat $f/_forest_proba.txt | grep -E -o '^[{]*\(S=\#i\[P=[0-9]+\.[0-9]*[-e]*[0-9]*\]' | grep -E -o '[0-9]+\.[0-9]*[-e]*[0-9]*' > $f/_output.txt

        #sum to get log-likelihood from file $output
        likelihood=$(python $DIR/sum_log_probabilities.py $f/_output.txt | sed 's/.*\[\(.*\)\].*/\1/' | tr -d ' ')
        echo " ->> likelihood:  "$likelihood

        # annotate parses
        cat $f/_forest.txt | sed 's/\((L[^ ]*\) /\1-H /g' | sed 's/\([^ _]_L\) /\1-H /g' | sed 's/\((R[^_]_[^ ]*\) /\1-H /g' | sed 's/^(S (\([^ ]*\) /(S (\1-H /g' | sed 's/\(_[lr]\)/\1-H/g' > $f/parses_head.txt
#        cat $f/_forest.txt | sed 's/\((L[^ ]*\) /\1-H /g' | sed 's/\((R[^ ]*\) /\1-H /g' | sed 's/\(_[lr]\)/\1-H/g' > $f/parses_head.txt

        python $DIR/transform_parses.py $f/parses_head.txt > $f/dep_parses.txt
        accuracy=$(python $DIR/evaluateD.py $f/dep_parses.txt ././wsj10.txt.gold | sed 's/.*\[\(.*\)\].*/\1/' | tr -d ' ')


        if [ $i -eq 1 ] ;
		then
			echo "iteration,likelihood,accuracy" >> $f/results.csv
		fi
		echo "#"$i","$likelihood","accuracy >> $f/results.csv
	done

