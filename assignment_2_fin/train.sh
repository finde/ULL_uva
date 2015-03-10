#!/usr/bin/env bash

#/bin/bash

input_treebank=$1

sentences=$(echo "$input_treebank" | sed 's/$/_sentences/g')
combined_numbers=$(echo "$input_treebank" | sed 's/$/_numbers/g')
all_numbers=$(echo "$input_treebank" | sed 's/$/_alphabetic_numbers/g')
clean_numbers=$(echo "$input_treebank" | sed 's/$/_clean_numbers/g')



if [ ! -e  $sentences ] ; then
	echo 'Creating sentences from treebank ' $input_treebank
	less $input_treebank | awk '{
	s=""
	for (i=1;i<=NF;i++) {
		if ($i ~ /\"([^"\)]+)\"/) {
			printf "%s",$i
			s=" "
		}
	}
	print ""
}' | sed -E 's/["\)]+/ /g ; s/^ //g' > $sentences
fi

if [ ! -e  $combined_numbers ] ; then
	echo 'Creating only numerals from ' $sentences
	less $sentences | grep -E -o "([0-9.,]+|one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve|thirteen|fourteen|fifteen|sixteen|seventeen|eighteen|nineteen|twenty|twenty-one|twenty-two|twenty-three|twenty-four|twenty-five|twenty-six|twenty-seven|twenty-eight|twenty-nine|thirty|thirty-one|thirty-two|thirty-three|thirty-four|thirty-five|thirty-six|thirty-seven|thirty-eight|thirty-nine|forty|forty-one|forty-two|forty-three|forty-four|forty-five|forty-six|forty-seven|forty-eight|forty-nine|fifty|fifty-one|fifty-two|fifty-three|fifty-four|fifty-five|fifty-six|fifty-seven|fifty-eight|fifty-nine|sixty|sixty-one|sixty-two|sixty-three|sixty-four|sixty-five|sixty-six|sixty-seven|sixty-eight|sixty-nine|seventy|seventy-one|seventy-two|seventy-three|seventy-four|seventy-five|seventy-six|seventy-seven|seventy-eight|seventy-nine|eighty|eighty-one|eighty-two|eighty-three|eighty-four|eighty-five|eighty-six|eighty-seven|eighty-eight|eighty-nine|ninety|ninety-one|ninety-two|ninety-three|ninety-four|ninety-five|ninety-six|ninety-seven|ninety-eight|ninety-nine) (hundred|thousand|million|billion)*" | sed -E 's/[,]//g' > $all_numbers
	less $all_numbers | grep -E -o '[0-9]+' > $clean_numbers
	less $all_numbers | sed -E 's/ten/10/g; s/eleven/11/g; s/twelve/12/g; s/thirteen/13/g; s/fourteen/14/g; s/fifteen/15/g; s/sixteen/16/g; s/seventeen/17/g; s/eighteen/18/g; s/nineteen/19/g; s/twenty/20/g; s/twenty-one/21/g; s/twenty-two/22/g; s/twenty-three/23/g; s/twenty-four/24/g; s/twenty-five/25/g; s/twenty-six/26/g; s/twenty-seven/27/g; s/twenty-eight/28/g; s/twenty-nine/29/g; s/thirty/30/g; s/thirty-one/31/g; s/thirty-two/32/g; s/thirty-three/33/g; s/thirty-four/34/g; s/thirty-five/35/g; s/thirty-six/36/g; s/thirty-seven/37/g; s/thirty-eight/38/g; s/thirty-nine/39/g; s/forty/40/g; s/forty-one/41/g; s/forty-two/42/g; s/forty-three/43/g; s/forty-four/44/g; s/forty-five/45/g; s/forty-six/46/g; s/forty-seven/47/g; s/forty-eight/48/g; s/forty-nine/49/g; s/fifty/50/g; s/fifty-one/51/g; s/fifty-two/52/g; s/fifty-three/53/g; s/fifty-four/54/g; s/fifty-five/55/g; s/fifty-six/56/g; s/fifty-seven/57/g; s/fifty-eight/58/g; s/fifty-nine/59/g; s/sixty/60/g; s/sixty-one/61/g; s/sixty-two/62/g; s/sixty-three/63/g; s/sixty-four/64/g; s/sixty-five/65/g; s/sixty-six/66/g; s/sixty-seven/67/g; s/sixty-eight/68/g; s/sixty-nine/69/g; s/seventy/70/g; s/seventy-one/71/g; s/seventy-two/72/g; s/seventy-three/73/g; s/seventy-four/74/g; s/seventy-five/75/g; s/seventy-six/76/g; s/seventy-seven/77/g; s/seventy-eight/78/g; s/seventy-nine/79/g; s/eighty/80/g; s/eighty-one/81/g; s/eighty-two/82/g; s/eighty-three/83/g; s/eighty-four/84/g; s/eighty-five/85/g; s/eighty-six/86/g; s/eighty-seven/87/g; s/eighty-eight/88/g; s/eighty-nine/89/g; s/ninety/90/g; s/ninety-one/91/g; s/ninety-two/92/g; s/ninety-three/93/g; s/ninety-four/94/g; s/ninety-five/95/g; s/ninety-six/96/g; s/ninety-seven/97/g; s/ninety-eight/98/g; s/ninety-nine/99/g; s/one/1/g; s/two/2/g; s/three/3/g; s/four/4/g; s/five/5/g; s/six/6/g; s/seven/7/g; s/eight/8/g; s/nine/9/g; s/hundred/00/g; s/thousand/000/g; s/million/000000/g; s/billion/000000000/g' | grep -E '[0-9]' | sed 's/ //g' > $combined_numbers
fi

python assignment_2a.py $combined_numbers $2

rm -f results_assignment_2a.zip
zip results_assignment_2a.zip ./*.png

rm ./*.png