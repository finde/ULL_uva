#!/bin/bash

treebank=$1
number_of_sentences=$2

echo "::Preparation::"
echo " - limiting treebanks to $number_of_sentences sentences"
head -n $number_of_sentences $treebank > new_treebank
cat new_treebank | sed 's/"//g' > new_treebank_gold

echo " - creating corpus from treebank"
cat new_treebank | sed 's/$/""\n/' | grep -E -o '"[^"]*"' | sed 's/"//g' > _corpus
# cat new_treebank | sed 's/$/""\n/' | grep -E -o '"[^"]*"' | sed 's/""//g' > _corpus

echo "::Extracting grammars::"
echo " - running PCFG extractor .."
java -jar ../PCFG_extractor.jar new_treebank _treebanks.grammar

echo " - Rearrange information such that it becomes suitable for Bitpar"
less _treebanks.grammar | sed 's/%/%%/g' | awk '{printf ($NF " "); for (i=1; i<NF; i++) printf ($i " "); printf ("\n");}' > _treebanks.grammar.bitpar
less _treebanks.grammar.bitpar | grep -E '"[^"]+"' | sed 's/\"//g' | awk '{print($3"\t"$2"\t"$1)}' > _treebanks.lexicon.bitpar
sed -i '' 's/"//g' _treebanks.grammar.bitpar

# Do a single pass of io with bitpar
echo " - do a single pass of io with bitpar"
bitpar -s TOP _treebanks.grammar.bitpar _treebanks.lexicon.bitpar _corpus -em em

# # remove lines with 0 counts
echo " - remove empty lines"
less em.gram | grep -v '0\.00' > em.grammar
less em.lex | grep -v '0\.000*' | awk '{print $1"\t"$2" "$3 }' > em.lexicon

echo " - parse again"
bitpar -s TOP em.grammar em.lexicon _corpus -b 1 > _parsed
cat _parsed | sed -i '' 's/\\//g' _parsed

echo " - running evalC"
java -jar ../evalC/evalC.jar new_treebank_gold _parsed _eval

# # get probabilities and write to file $output
# cat $parse_forests | grep -E -o '^[{]*\(TOP=\#i\[P=[0-9]+\.[0-9]*[-e]*[0-9]*\]' | grep -E -o '[0-9]+\.[0-9]*[-e]*[0-9]*' > $output

# # sum to get log-likelihood from file $output
# python sum_log_probabilities $output