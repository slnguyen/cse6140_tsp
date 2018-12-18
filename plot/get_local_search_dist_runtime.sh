#!/bin/bash

# $1 = alg
# $2 = num_itr
#bash get_local_search_dist_runtime.sh "2opt" 100

declare -a cities=("Atlanta" "Berlin" "Boston" "Champaign" "Cincinnati" "Denver"
                   "NYC" "Philadelphia" "Roanoke" "SanFrancisco" "Toronto" "UKansasState"
                   "ulysses16" "UMissouri")

trap "exit" INT
for i in "${cities[@]}"
do
echo $i
python ../code/run_ls_$1.py $i ../DATA/$i.tsp 0 $2
python -c "from plt_local_search import print_to_csv; print_to_csv('$1', $2, '$i')"


soln_qual=$( awk '{for(i=1;i<=NF;i++) {sum[i] += $i; sumsq[i] += ($i)^2}} 
          END {for (i=1;i<=NF;i++) {
          printf "%f +/- %f \n", sum[i]/NR, sqrt((sumsq[i]-sum[i]^2/NR)/(NR-1))}
         }' ../temp_output/$1/$i/$1_soln_qual.csv)

runtime=$( awk '{for(i=1;i<=NF;i++) {sum[i] += $i; sumsq[i] += ($i)^2}} 
          END {for (i=1;i<=NF;i++) {
          printf "%f +/- %f \n", sum[i]/NR, sqrt((sumsq[i]-sum[i]^2/NR)/(NR-1))}
         }' ../temp_output/$1/$i/$1_runtime.csv)

echo "$1 TSP distance: $soln_qual, elapsed time(ms): $runtime"
echo

done
