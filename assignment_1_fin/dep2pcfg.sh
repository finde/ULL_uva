#!/bin/bash

function split_head_g1 {
	awk '
	function root(h)
	{
		printf("S Y_%s\n",h);
		printf("Y_%s L_%s R_%s\n",h,h,h);
	}
	function left(h,a)
	{
		printf("L_%s Y_%s L_%s\n",h,a,h);
		printf("L_%s %s_l\n",h,h);
	}
	function right(h,a)
	{
	    printf("R_%s R_%s Y_%s\n",h,h,a);
		printf("R_%s %s_r\n",h,h);
	}
	{if ($1=="ROOT") root($2)
	else if($3=="left") left($1,$2)
	else right($1,$2)}'
}

function dmv {
	awk '
	function root(h)
	{
		printf("S Y_%s\n",h);
		printf("Y_%s L_%s R_%s\n",h,h,h);

		printf("L_%s %s_l\n",h,h);
		printf("LP_%s %s_l\n",h,h);
		printf("L_%s L1_%s\n",h,h);
		printf("LP_%s L1_%s\n",h,h);

        printf("R_%s %s_r\n",h,h);
		printf("RP_%s %s_r\n",h,h);
	    printf("R_%s R1_%s\n",h,h);
		printf("RP_%s R1_%s\n",h,h);
	}
	function left(h,a)
	{
		printf("L1_%s Y_%s LP_%s\n",h,a,h);
	}
	function right(h,a)
	{
	    printf("R1_%s RP_%s Y_%s\n",h,h,a);
	}
	{if ($1=="ROOT") root($2)
	else if($3=="left") left($1,$2)
	else right($1,$2)}'
}

function evg {
	awk '
	function root(h)
	{
		printf("S L_%s R_%s\n",h,h,h);

		printf("R_%s R0_%s\n",h,h);
		printf("R_%s RP_%s\n",h,h);
		printf("RP_%s R1_%s\n",h,h);
		printf("RP_%s R2_%s\n",h,h);

		printf("L_%s L0_%s\n",h,h);
		printf("L_%s LP_%s\n",h,h);
		printf("LP_%s L1_%s\n",h,h);
		printf("LP_%s L2_%s\n",h,h);

		printf("L0_%s %s_l\n",h,h);
        printf("R0_%s %s_r\n",h,h);
    }
	function left(h,a)
	{
		printf("L2_%s Y_%s LP_%s\n",h,a,h);
		printf("L1_%s Y_%s L0_%s\n",h,a,h);
	}
	function right(h,a)
	{
		printf("R2_%s RP_%s Y_%s\n",h,h,a);
		printf("R1_%s R0_%s Y_%s\n",h,h,a);
	}
	{if ($1=="ROOT") root($2)
	else if($3=="left") left($1,$2)
	else right($1,$2)}'
}

function fold_unfold {
	awk '
    function root(h)
    {
        printf("S L_%s R_%s\n",h,h,h);
        printf("L_%s %s_l\n",h,h);
        printf("R_%s %s_r\n",h,h);
    }
    function left(h,a)
    {
        printf("L_%s L_%s %s_M_%s\n",h,a,a,h);
        printf("L_%s %s_l\n",a,a);
        printf("%s_M_%s R_%s L_%s\n",a,h,a,h);
        printf("R_%s %s_r\n",a,a);
    }
    function right(h,a)
    {
        printf("R_%s %s_M_%s R_%s\n",h,h,a,a);
        printf("R_%s %s_r\n",a,a);
        printf("%s_M_%s R_%s L_%s\n",h,a,h,a);
        printf("L_%s %s_l\n",a,a);
    }
    {if ($1=="ROOT") root($2)
    else if($3=="left") left($1,$2)
    else right($1,$2)}'
}
