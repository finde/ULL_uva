#!/bin/bash
set -e

treebank=$1
number_of_sentences=$2
n_iteration=$3
DIR=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )
bitpar=$DIR'/../BitPar/src/bitpar'
output_folder=$DIR/$4

#. $DIR/preparation.sh
#. $DIR/grammar_extraction_pcfg.sh
#. $DIR/em.sh
. $DIR/headden_transform.sh

f='output'
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

################################################################################
## Extract POS-tag sequences from a treebank $treebank and write them to a file called $output
cat $treebank | sed '/^$/d' | sed -n '2p' | sed  -e 's/(/((/g;s/([^"]*(//g;s/ "[^)]*//g;s/)//g' > $sentence_file
## sed -e 's/(/((/g;s/([^()]\+ (//g;s/[^ ()]\+)//g;s/[()]//g;s/ \+/ /g;s/^ \+//'

#################################################################################
## Filtering out sentences with up to 10 tags
cat $sentence_file | awk '{if (NF<11) print}' > $sentences

#################################################################################
## Extract all dependencies from a file with sentences of words or POS tags

## extract all possible dependencies
cat $sentences |  awk '{for (i=1;i<=NF;i++) {print "ROOT",$i, "right"; for (j=i+1;j<=NF;j++) {print $i,$j, "right"; print $j,$i, "left"}}}' > $all_dependencies

## sort, count and sort again
cat $all_dependencies | sort | uniq -c | sort -g -r -k 1 | sed 's/ *[0-9]* //' | headden_transform | sort > $headden_transform
#
#################################################################################
## Annotate dependency parses encoded as CF-trees with Headden's transform with heads
cat $headden_transform | uniq -c | sed 's/^ \+//' > $grammar
cat $grammar | grep -E '\[l\]|\[r\]' | awk '{printf("%s\t%s\t%s\n",$3,$2,$1)}' > $lexicon

# convert sentences to double -> split head
cat $sentences | awk '{for (i=1;i<=NF;i++){printf("%s\n",$i)}printf("\n")}' > $corpus
cat $sentences | awk '{for (i=1;i<=NF;i++){printf("%s[l]\n%s[r]\n",$i,$i)}printf("\n")}' > $sentences_double

$bitpar -s TOP -q $grammar $lexicon $corpus -em $em

less $em.gram | grep -v '0\.00' > $em.grammar
less $em.lex | grep -v '0\.000*' | awk '{print $1"\t"$2" "$3 }' > $em.lexicon

rm -f $em.gram && rm -f $emm.lex
mv $em.grammar $em.gram
mv $em.lexicon $em.lex

$bitpar -s TOP -b 1 $em.gram $em.lex $corpus> $f/_forest
sed -i '' 's/\\//g' $f/_forest

echo "evaluation"
$bitpar -ip -s TOP $em.gram $em.lex $corpus> $f/_forest_proba
cat $f/_forest_proba | grep -E -o '^[{]*\(TOP=\#i\[P=[0-9]+\.[0-9]*[-e]*[0-9]*\]' | grep -E -o '[0-9]+\.[0-9]*[-e]*[0-9]*' > $f/_output

# sum to get log-likelihood from file $output
likelihood=$(python $DIR/sum_log_probabilities.py $f/_output | sed 's/.*\[\(.*\)\].*/\1/' | tr -d ' ')
echo " ->> likelihood:  "$likelihood

# annotate parses
#cat $Headden_parses | sed 's/\((L[^ ]\+\) /\1-H /g' | sed 's/\([^ _]_L\) /\1-H /g' | sed 's/\((R[^_]_[^ ]\+\) /\1-H /g' | sed 's/^(S (\([^ ]\+\) /(S (\1-H /g' | sed 's/\(_[lr]\)/\1-H/g' > parses_head
