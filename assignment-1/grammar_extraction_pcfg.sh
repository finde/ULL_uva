#!/bin/bash

function grammar_extraction_pcfg {
	f=$1
	echo "::Extracting grammars with PCFG::"
	echo " >> running PCFG extractor .."
	java -jar ../PCFG_extractor.jar $f/new_treebank $f/_treebanks.grammar

	echo " >> Rearrange information such that it becomes suitable for Bitpar"
	less $f/_treebanks.grammar | sed 's/%/%%/g' | awk '{printf ($NF " "); for (i=1; i<NF; i++) printf ($i " "); printf ("\n");}' > $f/em.gram
	less $f/em.gram | grep -E '"[^"]+"' | sed 's/\"//g' | awk '{print($3"\t"$2"\t"$1)}' > $f/em.lex
	sed -i '' 's/"//g' $f/em.gram
}
