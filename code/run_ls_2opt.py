'''
Code to get runtime of 2opt and write to files. File stored in 'temp_output' directory
python run_ls_2opt.py Boston ../../DATA/Boston.tsp 0
'''

import sys
#from .ls_2opt import get_2opt_dist
#from .file_io import get_edges_from_file
from ls_2opt import get_2opt_dist
from file_io import get_edges_from_file
import random
import os

def write_file(num_itr, incumbet_vals, city):
    if num_itr < 10:
        filename = '../temp_output/2opt/%s/2opt_00%s.txt' % (city, num_itr)
    elif num_itr < 100:
        filename = '../temp_output/2opt/%s/2opt_0%s.txt' % (city, num_itr)
    else:
        filename = '../temp_output/2opt/%s/2opt_%s.txt' % (city, num_itr)

    #check if output directory exists
    if not os.path.exists(os.path.dirname(filename)):
        try:
            os.makedirs(os.path.dirname(filename))
        except OSError as exc:
            if exc.errno != errno.EEXIST:
                raise

    with open(filename, 'w') as fp:
        fp.write('\n'.join('{},{}'.format(x[0],x[1]) for x in incumbet_vals)) 

    return

def run_ls_2opt(datafile, cutoff_time, random_seed):

    city = datafile.split('/')[-1].split('.')[0]
    input_file = datafile
    num_iter = cutoff_time
    seed = random_seed

    # num_iter = 100

    edge_list, num_nodes = get_edges_from_file(input_file)
    # from IPython import embed; embed()
    
    # continue iterating until there have been no improvements for 
    #'no_improvement_thresh' number of iterations
    no_improvement_thresh = 2000  
    log_incumbent = True         #flag to log incumbent values

    #run ls_2opt 'num_iter' number of times
    for i in range(num_iter):
        seed = seed+1	#use different random seed each iteration
        random.seed(seed)
        ls_2opt_dist, incumbent_vals = get_2opt_dist(edge_list, num_nodes, no_improvement_thresh)
        write_file(i, incumbent_vals, city)

    #print('ls_2opt distance: %s' %(ls_2opt_dist))

def main():
    city = sys.argv[1]
    datafile = sys.argv[2]
    seed = int(sys.argv[3])
    num_iter = int(sys.argv[4])

    run_ls_2opt(datafile, num_iter, seed)

if __name__ == "__main__":
    main()
