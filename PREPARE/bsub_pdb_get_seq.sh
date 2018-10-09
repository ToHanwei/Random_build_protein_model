#!/bin/sh

echo "
     +++++++++++++++++++++++++++++++++++++++++++
     +    From PDB format extract sequence     +
     + +++++++++++++++++++++++++++++++++++++++++
"

#echo -n "Input PDB fold: "
#read pdb
pdb="./PDB_MM_CLEAR"

#inputa fold that save sequence
#echo -n "Input fold that save sequence: "
#read fold
fold="BSUB_PDB_MM_SEQ"
mkdir ${fold}

declare -A resdic
resdic=(["GLY"]="G" ["ALA"]="A" ["VAL"]="V" ["LEU"]="L" 
["ILE"]="I" ["PRO"]="P" ["PHE"]="F" ["TYR"]="Y" ["TRP"]="W" 
["SER"]="S" ["THR"]="T" ["CYS"]="C" ["MET"]="M" ["ASN"]="N" 
["GLN"]="Q" ["ASP"]="D" ["GLU"]="E" ["LYS"]="K" ["ARG"]="R" 
["HIS"]="H")

for file in `ls $pdb`; do
    ff=${file:0:4}
    filename=${fold}"/"$ff".fasta"
    printf ">"`echo $file | cut -b 1-4` >> $filename
	printf " " >> $filename
    if test -f $pdb/$file; then
        num=1
        cat $pdb/$file | while read line; do
            name=`echo "$line" | cut -b 1-6`
            if [ $name = "ATOM" ]; then
                res=`echo "$line" | cut -b 18-20`
                res=${resdic[$res]}
                resid=`echo "$line" | cut -b 23-26`
                if [ $num -eq 1 ]; then
                    printf $res >> $filename
                    temp=$resid
                    let num+=1
                elif [ $resid -ne $temp ]; then
                    printf $res >> $filename
                    temp=$resid
                    let num+=1
					##Every line 60 character
                    #mod=$(($num%60))
                    #if [ $mod -eq 0 ]; then
                    #    echo "" >> $filename
                    #fi
                fi
            fi
        done
    else
        echo "$file not a file"
    fi
printf "\n" >> $filename
echo "$file is done!!!!"
done
