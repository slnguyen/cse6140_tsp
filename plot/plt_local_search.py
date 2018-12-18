'''
generate runtime plots
python plt_local_search.py 2_opt 100 Boston ../../DATA/Boston.tour
'''

import sys
import numpy as np
from scipy.interpolate import interp1d
import matplotlib.pyplot as plt

#print runtime and soln qual to csv for boxplot
def print_to_csv(alg, num_itr, city):
    runtime = []
    soln_qual = []
    out_file = '../temp_output/%s/%s/%s_runtime.csv' % (alg, city, alg)
    soln_qual_file = '../temp_output/%s/%s/%s_soln_qual.csv' % (alg, city, alg)

    for i in range(0,num_itr): #go through all iterations
        if i < 10:
            filename = '../temp_output/%s/%s/%s_00%s.txt' % (alg, city, alg, i)
        elif i < 100:
            filename = '../temp_output/%s/%s/%s_0%s.txt' % (alg, city, alg, i)
        else:
            filename = '../temp_output/%s/%s/%s_%s.txt' % (alg, city, alg, i)

        fh=open(filename, 'r')
        runtime.append(fh.readlines()[-1].split(',')[0]) #get last line from file
        fh.close()

        fh=open(filename, 'r')
        soln_qual.append(fh.readlines()[-1].split(',')[1]) #get last line from file
        fh.close()  

    with open(out_file, 'w') as fp:
        fp.write('\n'.join('{}'.format(float(x)*1000) for x in runtime))  #print time in ms 

    with open(soln_qual_file, 'w') as fp:
        fp.write('\n'.join('{}'.format(float(x)) for x in soln_qual))  #print time in ms 

    return 0
#get min and max times for interpolation
def get_time_bounds(alg, num_itr, city):

    min_time = 0.0
    max_time = 0.0
    for i in range(0,num_itr): #go through all iterations
        if i < 10:
            filename = '../temp_output/%s/%s/%s_00%s.txt' % (alg, city, alg, i)
        elif i < 100:
            filename = '../temp_output/%s/%s/%s_0%s.txt' % (alg, city, alg, i)
        else:
            filename = '../temp_output/%s/%s/%s_%s.txt' % (alg, city, alg, i)

        
        fh=open(filename, 'r')
        temp_min = float(fh.readlines()[0].split(',')[0])
        min_time = temp_min if temp_min > min_time else min_time #first line in file of the form 'elapsed time,distance', get lower time bound which is max of first line between files
        fh.close()

        fh=open(filename, 'r')
        temp_max =  float(fh.readlines()[-1].split(',')[0])
        max_time = temp_max if temp_max > max_time else max_time #last line in file of the form 'elapsed time,distance', get upper time bound which is max of last line between files
        fh.close()  

    return min_time, max_time


def get_interpolated_dist(alg, num_itr, min_time, max_time, city):

    dist_interp = []
    time_interp = np.linspace(float(min_time), float(max_time), num=1000, endpoint=True)

    for i in range(0,num_itr): #go through all iterations
        if i < 10:
            filename = '../temp_output/%s/%s/%s_00%s.txt' % (alg, city, alg, i)
        elif i < 100:
            filename = '../temp_output/%s/%s/%s_0%s.txt' % (alg, city, alg, i)
        else:
            filename = '../temp_output/%s/%s/%s_%s.txt' % (alg, city, alg, i)

        time = []
        dist = []        
        fh=open(filename, 'r')
        for line in fh:
            time.append(float(line.strip().split(',')[0]))
            dist.append(float(line.strip().split(',')[1]))
        fh.close()
        dist_interp.append(np.interp(time_interp, time, dist))

    return time_interp, np.array(dist_interp)


def main():
    alg = sys.argv[1] #e.g. 'ls_2opt_dist'
    num_itr = int(sys.argv[2])
    city = sys.argv[3]
    opt_soln_filename = sys.argv[4]



########################################################
#
#Below is code for printing runtime and solution qual to CSV for box plots
#
########################################################

    print_to_csv(alg, num_itr, city)

########################################################
#
#Below is code for generating QRTD and SQD Plots
#
########################################################
    min_time, max_time = get_time_bounds(alg, num_itr, city) #get min and max times for interpolation
    interp_time, interp_dist = get_interpolated_dist(alg, num_itr, min_time, max_time, city) #interp dist = [rows, cols, vals] = [instance, time, distances] (i.e. [[distance across time for instance 1]. [ distance across time instance 2], [distance across time instance 3]], ...)
    interp_time = interp_time*1000 #convert to miliseconds


#get optimal solution
    fh=open(opt_soln_filename, 'r')
    opt_soln = int(fh.readline())
    fh.close


    rtd_plot=[]
    opt_mult = np.linspace(1.0, 1.3, num=100, endpoint=True) #optimal solution multiplier
    rel_sol_qual = opt_mult-1.0
    for i in range(len(opt_mult)):
        rtd_score = interp_dist <= opt_mult[i]*opt_soln #get rtd for given score
        rtd_plot.append(np.sum(rtd_score, axis=0)/float(num_itr)) #count number of instances that are less than the multiplier*optimum_solutiom

    rtd_plot = np.array(rtd_plot)
    # from IPython import embed; embed()
#plot of time vs probability of instances being less than a given distance (i.e. 1.0*optimal_distnace, 1.6*optimal_distance, 2.5*optimal_distance, etc.) (QRTD)
    plt.figure(0)
    plt.plot(interp_time, rtd_plot[0])
    plt.plot(interp_time, rtd_plot[20])
    plt.plot(interp_time, rtd_plot[40])
    plt.plot(interp_time, rtd_plot[60])
    plt.plot(interp_time, rtd_plot[80])
    plt.plot(interp_time, rtd_plot[99])
    plt.legend([rel_sol_qual[0], '{0:.2f}'.format(rel_sol_qual[20]), '{0:.2f}'.format(rel_sol_qual[40]), '{0:.2f}'.format(rel_sol_qual[60]), '{0:.2f}'.format(rel_sol_qual[80]), '{0:.2f}'.format(rel_sol_qual[99])])
    plt.xlim(right=5)
    plt.xlabel('Time (ms)', fontsize=16)
    plt.ylabel('Probability', fontsize=16)
    plt.ylim(-0.1, 1.1)
    plt.xlim(-1, max_time*1000)

#plot probability of instances being less than a distance (i.e. 1.0*optimal_distnace, 1.6*optimal_distance, 2.5*optimal_distance, etc.) for a given runtime (SQD)
    plt.figure(1)
    plt.plot(rel_sol_qual, rtd_plot[:, 25])
    plt.plot(rel_sol_qual, rtd_plot[:, 50])
    plt.plot(rel_sol_qual, rtd_plot[:, 100])
    plt.plot(rel_sol_qual, rtd_plot[:, 200])
    plt.plot(rel_sol_qual, rtd_plot[:, 400])
    plt.plot(rel_sol_qual, rtd_plot[:, 800])
    plt.legend(['{0:.2f} ms'.format(interp_time[25]), '{0:.2f} ms'.format(interp_time[50]), '{0:.2f} ms'.format(interp_time[100]), '{0:.2f} ms'.format(interp_time[200]), '{0:.2f} ms'.format(interp_time[400]), '{0:.2f} ms'.format(interp_time[800])])
#plt.xlim(right=2.5)
    plt.xlabel('Relative solution quality', fontsize=16)
    plt.ylabel('Probability', fontsize=16)

    plt.show()

if __name__ == "__main__":
    main()
