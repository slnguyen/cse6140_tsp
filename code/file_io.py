import math
import re
import sys
from collections import defaultdict

#get number of line that contains keyword
def get_line_num(filename, keyword):
    fh=open(filename, 'r')
    line_counter = 1
    for line in fh:
        if re.match(keyword, line):
            fh.close()
            return line_counter
        line_counter += 1
    assert False, "line not found"

#edge list will contain (n)(n+1)/2 edges
def generate_edge_list_euc(coord_list):
    edge_list = []
    len_list = len(coord_list)
    for coord_ind1 in range(len_list-1):
        coord1 = [float(x) for x in coord_list[coord_ind1].split()]             #coord1 = [ID, x_coord, y_coord]
        for coord_ind2 in range(coord_ind1+1,len_list):                 
            coord2 = [float(x) for x in coord_list[coord_ind2].split()]
            dist = int(round(math.sqrt((coord1[1]-coord2[1])**2 + (coord1[2]-coord2[2])**2)))       #sqrt((x1-x2)^2 + (y1-y2)^2)
            edge_list.append((int(coord1[0]), int(coord2[0]), dist))
    return edge_list

def generate_edge_list_geo(coord_list):
#from www.iwr.uni-heidelberg.de/groups/comopt/software/TSPLIB95/DOC.PS pg 7
#and FAQ: https://www.iwr.uni-heidelberg.de/groups/comopt/software/TSPLIB95/TSPFAQ.html
    def convert(coord):
        PI = 3.141592
        coord = float(coord)
        #deg = int(math.floor(coord)) #does not generate correct result for negative coord (eg -5.21)?
        deg = int(coord)
        minutes = coord - deg
        val = PI * (deg + 5.0 * minutes / 3.0 ) / 180.0
        return val

    def get_lat_long(coord_list):
        latitudes = [convert(coord_list[i].split()[1]) for i in range(len(coord_list))]
        longitudes = [convert(coord_list[i].split()[2]) for i in range(len(coord_list))]
        return latitudes, longitudes

    edge_list = []
    len_list = len(coord_list)
    latitudes, longitudes = get_lat_long(coord_list)
    

    RRR = 6378.388    
    for coord_ind1 in range(len_list-1):
        for coord_ind2 in range(coord_ind1+1,len_list):
            q1 = math.cos(longitudes[coord_ind1] - longitudes[coord_ind2])
            q2 = math.cos(latitudes[coord_ind1] - latitudes[coord_ind2])
            q3 = math.cos(latitudes[coord_ind1] + latitudes[coord_ind2])
            dist = int((RRR * math.acos(0.5*((1.0+q1)*q2 - (1.0-q1)*q3)) + 1.0))
            edge_list.append((int(coord_list[coord_ind1].split()[0]), int(coord_list[coord_ind2].split()[0]), dist))

    return edge_list


def get_file_format(filename):
    keyword = 'EDGE_WEIGHT_TYPE'
    fh=open(filename, 'r')
    for line in fh:
        if re.match(keyword, line):
            return(line.split()[1])
            fh.close()
    assert False, "line not found"

#function to get edges from given list of coordinates (input file)
def get_edges_from_file(filename):

    file_format = get_file_format(filename)

    start_line_num = get_line_num(filename, "NODE_COORD_SECTION")
    end_line_num = get_line_num(filename, "(.*)EOF")-1

    fh=open(filename, 'r')
    coord_list = fh.readlines()[start_line_num:end_line_num] #list of coordinates
    fh.close()

    if(file_format == "EUC_2D"):
        edge_list = generate_edge_list_euc(coord_list)   #each element of edge_list is a tuple containing vertex and weight (i.e. (u, v, weight))
    if(file_format == "GEO"):
        edge_list = generate_edge_list_geo(coord_list)   #each element of edge_list is a tuple containing vertex and weight (i.e. (u, v, weight))
    return edge_list, len(coord_list)
