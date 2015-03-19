#!/usr/bin/env bash
file=$1
threshold=$2
cat $file | tr ' ' '\n' | cut -d "/" -f 1  | grep '[$a-zA-Z0-9].*' | sort | uniq -c | sort -r | awk '($1 > "'${threshold}'"){print $2}'