#!/bin/bash

treebank=$1
corpus=$2

# Uniquely number all nonterminals (except for TOP)
echo "create a treebank with unique non-terminals"
cat $treebank | sed 's/\([A-Z\$]\) /\1-NR- /g' | awk '{ while($0~/-NR-/) sub(/-NR-/, ++cnt); print}' | sed 's/TOP[0-9]*/TOP/g' > treebank_unique

# concatenate treebanks
echo "Concatenate with regular treebank"
cat treebank_unique $treebank > treebanks

# extract grammar
echo "create a PCFG with the PCFG extractor"
java -jar ./PCFG_extractor.jar treebanks treebanks.grammar

# rearrange and generate bitpar grammar and lexicon files
echo "Rearrange information such that it becomes suitable for Bitpar"
less treebanks.grammar | sed 's/%/%%/g' | awk '{printf ($NF " "); for (i=1; i<NF; i++) printf ($i " "); printf ("\n");}' > treebanks.grammar.bitpar

less treebanks.grammar.bitpar | grep -E '"[^"]+"' | sed 's/\"//g' | awk '{print($3"\t"$2"\t"$1)}' > treebanks.lexicon.bitpar

sed -i '' 's/"//g' treebanks.grammar.bitpar

# Do a single pass of io with bitpar
echo "Do a pass of io with bitpar"
bitpar -s TOP treebanks.grammar.bitpar treebanks.lexicon.bitpar $corpus -em em

# remove lines with 0 counts
echo "Remove empty lines"
less em.gram | grep -v '0\.00' > em.grammar
less em.lex | grep -v '0\.000*' | awk '{print $1"\t"$2" "$3 }' > em.lexicon

bitpar -s TOP em.grammar em.lexicon $corpus -em em