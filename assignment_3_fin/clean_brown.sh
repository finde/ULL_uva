#!/usr/bin/env bash
file=$1
output=$2
halfWindow=$3
rm -f $output 2> /dev/null
cat $file | sed 's/\/[^\ ]*/ /g' | tr '\t' '#' | tr '\n' '#' | tr ' ' '\n' | sed 's/#.*#/#/g' | grep "[$#a-zA-Z0-9][a-zA-Z0-9'-]*" | tr '\n' ' ' | tr '#' '\n' | awk '{if (NF>="'${halfWindow}'") print}' >> $2