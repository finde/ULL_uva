#!/bin/bash
set -e

treebank=$1
number_of_sentences=$2
n_iteration=$3
DIR=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )
bitpar=$DIR'/../BitPar/src/bitpar'
output_folder=$DIR/$4

. $DIR/preparation.sh
. $DIR/grammar_extraction_pcfg.sh
. $DIR/em.sh

########### MAIN FUNCTION  ################
preparation $treebank $number_of_sentences $output_folder
grammar_extraction_pcfg $output_folder
em $output_folder $n_iteration