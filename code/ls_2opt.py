'''
Local search 2-opt exchange algorithm for TSP
'''

import sys
from operator import itemgetter
from file_io import get_edges_from_file
from collections import defaultdict
import random
import time

#find the index of the edge in edge_list, u and v are between 1 and number of cities
def find_edge_index(u, v, num_nodes):

    #make u the smaller vertex index
    if u > v:
        v, u = u, v
    bias = 1+(u-2)*(u-1)//2 
    return (u-1)*(num_nodes-1)-bias+(v-u)  

#find total weight of path
def get_weight(path_list, edge_list, num_nodes):
    weight = 0
    for i in range(len(path_list)-1):
        u = path_list[i]
        v = path_list[i+1]
        weight += edge_list[find_edge_index(u, v, num_nodes)][2]
    return weight   


#find the weight when swaping paths
def weight_swap(path_list, edge_list, num_nodes, i, j):
    #path a
    a1 = path_list[i]    #edge u
    a2 = path_list[i+1]  #edge v

    #path b
    b1 = path_list[j]    #edge u
    b2 = path_list[j+1]  #edge v

    #find weight diff resulting from swapping
    remove_weight =  edge_list[find_edge_index(a1, a2, num_nodes)][2] + edge_list[find_edge_index(b1, b2, num_nodes)][2]
    add_weight = edge_list[find_edge_index(a1, b1, num_nodes)][2] + edge_list[find_edge_index(a2, b2, num_nodes)][2]
    return add_weight-remove_weight


def get_2opt_dist(edge_list, num_nodes, no_improvement_thresh):
    path_list = [i for i in range(1,num_nodes+1)]
    random.shuffle(path_list) #shuffle numbers from 1 to number of cities to create initial path
    path_list.append(path_list[0])
    orig_weight = get_weight(path_list, edge_list, num_nodes)
    updated_weight = orig_weight
    no_improvement_count = 0 #counter for number of iterations with no improvement
    incumbent_vals = []

    start = time.time()
    while no_improvement_count < no_improvement_thresh:
    #print('Before: %s' % path_list)
        p1 = random.randint(0, num_nodes-1)
        p2 = random.randint(0, num_nodes-1)

        if p1 > p2:
            p1, p2 = p2, p1 
        if p2-p1 > 1:

            weight_diff = weight_swap(path_list, edge_list, num_nodes, p1, p2)
            if (weight_diff < 0): #swapping decreaces weight
                path_list[p1+1:p2+1] = path_list[p2:p1:-1]
                updated_weight += weight_diff
                no_improvement_count = 0
            else:
                no_improvement_count += 1
        incumbent_vals.append((time.time() - start, updated_weight))

    return updated_weight, incumbent_vals


