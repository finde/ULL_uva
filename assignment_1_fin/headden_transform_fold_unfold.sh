#!/bin/sh
awk '
    function right(s){
        for (j=s+2;j<=NF;j++)
        {
            if ($j=="("substr($(s-1),2)+1)
            {
                return j+1;
            }
        }
    }

    function left(s){
        for (j=s;j<=NF;j++)
        {
            if ($j=="("substr($(s-1),2)+1)
            {
                return j+1;
            }
        }
    }

    function new_label(    i,    newleft,     newright){
        if (i in arr)
            return arr[i];

        else if ((!match($i,/\[/) && $i!="S") || (match($i,/\[/)&& match($(i+1),/\)/)) )
        {
            arr[i]=$i;
            return arr[i];
        }

        else if (match($i,/\[/) && match($(i+1),/\[/))
        {
            if (match($(i+1),/\[l\]/)){
                arr[i]="L["substr($(i+1),1,length($(i+1))-3)"]";
                return arr[i];
            }
            else{
                arr[i]="["substr($(i+1),1,length($(i+1))-3)"]R";
                return arr[i];
            }
        }

        else
        {
            newleft=new_label(left(i));
            newright=new_label(right(i));

            if (match(newleft,/L\[/) && match(newright,/\]R/))
            {
                arr[i]="S";
                printf "ROOT "substr(newleft,3,length(newleft)-3)" right\n";
                return arr[i];
            }

            else if (match(newleft,/\]M\[/))
            {
                idx=index(newleft,"]M[");
                arr[i]=substr(newleft,1,idx)"R"
                printf substr(newleft,2,idx-2)" "substr(newleft,idx+3,length(newleft)-(idx+3))" right\n";
                return arr[i];
            }

            else if (match(newright,/\]M\[/))
            {
                idx=index(newright,"]M[");
                arr[i]="L"substr(newright,idx+2);
                printf substr(newright,idx+3,length(newright)-(idx+3))" "substr(newright,2,idx-2)" left\n";
                return arr[i];
            }

            else if (match(newleft,/\]R/) && match(newright,/L\[/))
            {
                arr[i]=substr(newleft,1,length(newleft)-1)"M"substr(newright,2);
                return arr[i];
            }
        }
    }

    {
        for (i=1;i<=NF;i++)
        new_label(i);
        printf "\n";
        delete arr;
    }'
