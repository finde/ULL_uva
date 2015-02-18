#!/bin/bash
set -e

treebank=$1
number_of_sentences=$2
n_iteration=$3
output_folder=$4
bitpar='../BitPar/src/bitpar'

. preparation.sh
. grammar_extraction_pcfg.sh
. em.sh

########### MAIN FUNCTION  ################
preparation $treebank $number_of_sentences $output_folder
grammar_extraction_pcfg $output_folder
em $output_folder $n_iteration