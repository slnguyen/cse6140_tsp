#!/bin/bash


python ../code/run_ls_2opt.py Boston ../DATA/Boston.tsp 0 100
python plt_local_search.py 2opt 100 Boston ../DATA/Boston.tour


