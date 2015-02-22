#!/bin/bash

function split_head_g1 {
	awk '
	function root(h)
	{
		printf("S Y_%s\n",h,h);
		printf("Y_%s L_%s R_%s\n",h,h,h);
	}
	function left(h,a)
	{
		printf("L_%s Y_%s L_%s\n",h,a,h);
		printf("R_%s %s_r\n",a,a);
	}
	function right(h,a)
	{
	    printf("R_%s R_%s Y_%s\n",h,h,a);
		printf("L_%s %s_l\n",a,a);
	}
	{if ($1=="ROOT") root($2)
	else if($3=="left") left($1,$2)
	else right($1,$2)}'
}

function dmv {
	awk '
	function root(h)
	{
		printf("S Y_%s\n",h,h);
		printf("Y_%s L_%s R_%s\n",h,h,h);
	}
	function left(h,a)
	{
		printf("L_%s L0_%s\n",h,h);
		printf("L_%s L1_%s\n",h,h);
		printf("LP_%s L0_%s\n",h,h);
		printf("LP_%s L1_%s\n",h,h);
		printf("LP_%s Y_%s LP_%s\n",h,a,h);
		printf("L0_%s %s_l\n",h,h);
	}
	function right(h,a)
	{
	    printf("R_%s R0_%s\n",h,h);
		printf("R_%s R1_%s\n",h,h);
		printf("RP_%s R0_%s\n",h,h);
		printf("RP_%s R1_%s\n",h,h);
		printf("RP_%s RP_%s Y_%s\n",h,h,a);
		printf("R0_%s %s_r\n",h,h);
	}
	{if ($1=="ROOT") root($2)
	else if($3=="left") left($1,$2)
	else right($1,$2)}'
}
