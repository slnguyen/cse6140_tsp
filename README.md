# cse6140_tsp

### MST 2-approx:  <br />
To output runtime and solution quality for MST 2-approx, run:  <br />
```
bash get_mst_dist_runtime.sh
```
from the `/plot` directory. Output should look something like:  <br />
```
Atlanta
MST 2-approx TSP distance: 2756145, elapsed time(ms): 3.69310379028

Berlin
MST 2-approx TSP distance: 10603, elapsed time(ms): 11.589050293

Boston
MST 2-approx TSP distance: 1242717, elapsed time(ms): 5.59782981873
....
```

### Local search neighborhood 2-opt exchange: <br />
To output runtime and solution quality for local search neighborhood 2-opt exchange, run:  <br />
```
bash get_local_search_dist_runtime.sh "2opt" 100
```
from the `/plot` directory. Output should look something like:  <br />
```
Atlanta
2opt TSP distance: 2053901.580000 +/- 35262.824967 , elapsed time(ms): 7.288544 +/- 0.763090 

Berlin
2opt TSP distance: 8361.530000 +/- 273.846394 , elapsed time(ms): 19.683192 +/- 4.325759 

Boston
2opt TSP distance: 935291.560000 +/- 23641.387403 , elapsed time(ms): 14.298782 +/- 2.807561 
....
```

### Plot Qualified Runtime Distributions (QRTD) and Solution Quality Distributions (SQD) <br />
To plot QRTDs and SQDs for the local search neighborhood 2-opt exchange algorithm, run:
```
bash plt_local_search.sh
```

