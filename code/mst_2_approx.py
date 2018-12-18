'''
MST 2-approximation algorithm for TSP
'''

import sys
from operator import itemgetter
from file_io import get_edges_from_file
from collections import defaultdict
import time

class Node:
   def __init__(self, node_name):
       self.node_name =  node_name
   def __str__(self):
       return str(self.node_name)

#using pseudocode from CLRS 21.3
#union-find
def make_set(x):
    x.p = x
    x.rank = 0

def union(x, y):
    link(find_set(x), y)

def link(x, y):
    if x.rank > y.rank:
        y.p = x
    else: 
        x.p = y
        if x.rank == y.rank:
            y.rank = y.rank+1

def find_set(x):
    while (x != x.p):
        x.p = (x.p).p
        x = x.p
    return x


#radix sort from wikipedia
def radix_sort(array, base=10):
    def list_to_buckets(array, base, iteration):
        #create 10 buckets bc base 10
        buckets = [[] for x in range(base)]  
        for number in array:
            digit = (number[2] // (base ** iteration)) % base
            buckets[digit].append(number)
        return buckets

    def buckets_to_list(buckets):
        numbers = []
        for bucket in buckets:
            for number in bucket:
                numbers.append(number)
        return numbers

    maxval = max([x[2] for x in array])
    it = 0

    while base ** it <= maxval:

        array = buckets_to_list(list_to_buckets(array, base, it))
        it += 1
            
    return array


#compute MST
def computeMST(edge_list):
    mst_weight = 0
    mst_graph = {}
    #sort edges by weight in increasing order
    edge_list_sorted = radix_sort(edge_list) 
    #sorted(edge_list,key=itemgetter(2))  

    len_edge_list = len(edge_list)
    nodes = [Node(v) for v in range(len_edge_list)] #list of all nodes
    [make_set(node) for node in nodes]  #make each node its own set
    
    edge_count = 0
    while (edge_count < len(edge_list_sorted)):
        u_rep = find_set(nodes[edge_list_sorted[edge_count][0]])
        v_rep = find_set(nodes[edge_list_sorted[edge_count][1]])
        if (u_rep != v_rep):
            mst_graph.update({(edge_list_sorted[edge_count][0], edge_list_sorted[edge_count][1]): edge_list_sorted[edge_count][2]})
            mst_weight = mst_weight + edge_list_sorted[edge_count][2]
            union(u_rep, v_rep)
        edge_count = edge_count+1
    return mst_weight, mst_graph

#depth first search
def dfs(start_node, adj_dict):
    S = [(start_node, [start_node])]
    explored = [start_node]
    while S:
        (u, path) = S.pop()
        for v in (set(adj_dict[u]).difference(set(path))):
            S.append((v, path + [v]))
            explored.append(v)
    return explored

def run_mst_2_approx(datafile):
    #compute MST 2-approx TSP distance

    input_file = datafile
    edge_list, num_nodes = get_edges_from_file(input_file)

    start_time = time.time()
    mst_weight, mst_graph = computeMST(edge_list)

    #create dictionary (adj_dict) where key is a node of the MST and values are neighboring/adjacent nodes
    adj_dict = defaultdict(set)
    mst_edges = list(mst_graph.keys())
    for i in range(len(mst_edges)):
        adj_dict[mst_edges[i][0]].add(mst_edges[i][1])
        adj_dict[mst_edges[i][1]].add(mst_edges[i][0])

    #get dfs path
    dfs_path = dfs(1, adj_dict)
    dfs_path.append(dfs_path[0]) #need to append first vertex to create a cycle

    dist = 0 #TSP distnace
    for i in range(len(dfs_path)-1):
        u = dfs_path[i]
        v = dfs_path[i+1]
        #make u the smaller vertex index
        if u > v:
            v, u = u, v
        bias = 1+(u-2)*(u-1)//2 
        dist += edge_list[(u-1)*(num_nodes-1)-bias+(v-u)][2]
    end_time = time.time()
        
    print('MST 2-approx TSP distance: %s, elapsed time(ms): %s' %(dist, (end_time - start_time)*1000))

def main():
    datafile = sys.argv[1]

    run_mst_2_approx(datafile)

if __name__ == "__main__":
    main()

