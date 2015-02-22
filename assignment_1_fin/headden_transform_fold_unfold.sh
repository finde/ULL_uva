#!/bin/bash

function headden_transform {
	awk '
	function root(h)
	{
		printf("S L[%s] [%s]R\n",h,h);
		printf("L[%s] %s_L\n",h,h);
		printf("[%s]R %s_R\n",h,h);
	}
	function left(h,a)
	{
		printf("L[%s] L[%s] [%s]M[%s]\n",h,a,a,h);
		printf("L[%s] %s_L\n",a,a);
		printf("[%s]M[%s] [%s]R L[%s]\n",a,h,a,h);
		printf("[%s]R %s_R\n",a,a);
	}
	function right(h,a)
	{
		printf("[%s]R [%s]M[%s] [%s]R\n",h,h,a,a);
		printf("[%s]R %s_R\n",a,a);
		printf("[%s]M[%s] [%s]R L[%s]\n",h,a,h,a);
		printf("L[%s] %s_L\n",a,a);
	}
	{if ($1=="ROOT") root($2)
	else if($3=="left") left($1,$2)
	else right($1,$2)}'
}
