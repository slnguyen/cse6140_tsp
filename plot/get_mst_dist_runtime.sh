#!/bin/bash

declare -a cities=("Atlanta" "Berlin" "Boston" "Champaign" "Cincinnati" "Denver"
                   "NYC" "Philadelphia" "Roanoke" "SanFrancisco" "Toronto" "UKansasState"
                   "ulysses16" "UMissouri")


for i in "${cities[@]}"
do
echo $i
python ../code/mst_2_approx.py ../DATA/$i.tsp
echo 
done
