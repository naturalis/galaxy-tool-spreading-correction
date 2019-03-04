#!/bin/bash

#location for production server
#outlocation=$(mktemp -d /media/GalaxyData/database/files/XXXXXX)
#location for the testserver
#outlocation=$(mktemp -d /media/GalaxyData/files/XXXXXX)
outlocation=$(mktemp -d /home/galaxy/ExtraRef/XXXXXX)

python3 /home/galaxy/Tools/Spreading-Correction/create_input.py -t $1 -n $2 -ot $outlocation"/transposed.txt" -o $outlocation"/nextera_transposed.txt"
sed 's/\t/ /g' $outlocation"/nextera_transposed.txt" > $outlocation"/nextera_transposed_space.txt"

if [ "${8}" ]
then
  unspread_manual.py $outlocation"/nextera_transposed_space.txt" --i5 'S.index.name' --i7 'N.index.name' --column 0 --sep ' ' --rows $6 --cols $7 --c $9 --conditional_spreading_input "${8}" --output_folder $outlocation"/" > $outlocation"/log.txt"
  cat $outlocation"/log.txt" >> $outlocation"/log2.txt"
else
  unspread.py $outlocation"/nextera_transposed_space.txt" --i5 'S.index.name' --i7 'N.index.name' --column 0 --sep ' ' --rows $6 --cols $7 --h $8 --c $9 --t "${10}" --output_folder $outlocation"/" > $outlocation"/log.txt"
  cat $outlocation"/log.txt" $outlocation"/"*".log" >> $outlocation"/log2.txt"
fi

mv $outlocation"/log2.txt" $3
mv $outlocation"/"*".pdf" $4
[ -f $outlocation"/"*".csv" ] && mv $outlocation"/"*".csv" $5


rm -rf $outlocation
