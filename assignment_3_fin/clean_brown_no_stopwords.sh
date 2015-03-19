#!/usr/bin/env bash
file=$1
output=$2
rm -f $output 2> /dev/null
cat $file | sed 's/\/[^\ ]*/ /g' | sed 's/ //' | tr '[:upper:]' '[:lower:]' | tr '[:punct:]' ' ' | grep "[$#a-zA-Z0-9][a-zA-Z0-9'-]*" | tr '\n' '#' | tr -s '[:blank:]' '[\n*]' | tr '\n' ' ' | tr '#' '\n' | sed 's/ //' | awk '{if (NF>=2) print}' >> $2
