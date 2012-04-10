'''
Homework 9
Author: Cameron Bates

This script compares three different methods of computing pi. One method is
serial, one method uses multiprocessing, and one uses ipythons ipcluster 
method. Prior to running this an ipcluster must be started.  
'''

from time import time
from multiprocessing import cpu_count

def serial(number_of_darts):
    '''
    This function runs the basic serial dart throwing for the computation of
    pi for the input number of dart throws.
    '''
    from random import uniform
    from math import sqrt
    number_of_darts_in_circle = 0
    for n in range(number_of_darts):
        x, y = uniform(0,1), uniform(0,1)
        if sqrt((x - 0.5)**2 + (y - 0.5)**2) <= 0.5:
            number_of_darts_in_circle += 1
    return number_of_darts_in_circle

def serialpi(number_of_darts):
    #time the serial method
    start = time()
    serial(number_of_darts)
    stop = time()
    return stop-start

def calcdartspp(nproc,ndarts):
    #this is a helper method to split the darts per processor evenly while
    #making sure that the total number of darts computed is correct.
    dpp = []
    mod = ndarts % nproc
    rough = ndarts/nproc
    while ndarts != mod:
        ndarts -= rough
        dpp.append(rough)
    dpp[-1] += mod
    return dpp  

def multiprocessingpi(number_of_darts):
    #This function uses the multiprocessing module to parallelize the
    #serial computation    
    from multiprocessing import Pool  
    final = 0
    #get number of cores
    nproc = cpu_count()
    p = Pool(nproc)
    #start timing
    start = time()
    dartspp = calcdartspp(nproc,number_of_darts)
    #Use the map_async method to split the computation up
    result = p.map_async(serial,dartspp)
    result.wait()
    poolresult = result.get()
    #sum the final result
    for item in poolresult:
        final += item
    stop = time()
    #we don't use the final result we just care about the time
    
    #print 4*final/float(number_of_darts) 
    return stop-start

def ipcluster(number_of_darts):
    '''
    This method uses an ipython ipcluster to parallelize the serial
    computation of pi.
    '''
    #create a client
    from IPython.parallel import Client
    c = Client() 
    final = 0
    #determine the number of engines running
    nproc = len(c.ids)
    #start timing
    start = time()
    dartspp = calcdartspp(nproc,number_of_darts)
    #use the map_sync method to split the computation up
    result = c[:].map_sync(serial,dartspp)
    for item in result:
        final += item
    stop = time()
    
    return stop-start

if __name__ == '__main__':
    '''
    This main function runs the three different methods for various total 
    numbers of darts.
    '''
    import numpy as np
    #sizes to use
    n = [50,300,1000,5000,20000,100000,1000000,10000000]#np.logspace(2,7,8)
    n = np.array(n,dtype=int)
    #initialize result arrays
    mp = np.zeros(8)
    serialr = np.zeros(8)
    ipy = np.zeros(8)
    #Run seperately for more consistent results
    for index, item in enumerate(n):
        mp[index] = multiprocessingpi(item)
    for index, item in enumerate(n):
        ipy[index] = ipcluster(item)
    for index, item in enumerate(n):
        serialr[index] = serialpi(item)
        
    import matplotlib.pyplot as plt
    #calculate the darts per second for each method
    dpsmp = np.array(n)/mp
    dpsipy = np.array(n)/ipy
    dpsserialr = np.array(n)/serialr
    
    #plot the execution time as a function of the number of darts thrown
    fig = plt.figure()
    ax1 = fig.add_subplot(111)
    plt.plot(n,mp,'o-',label='multiprocessing')
    plt.hold(True)
    plt.plot(n,ipy,'o-',label='ipcluster')
    plt.loglog(n,serialr,'o-',label='serial')
    plt.xlabel('Number of Darts Thrown')
    plt.ylabel('Execution Time (Seconds), solid line')
    plt.legend(loc=2)
    
    #add a second axis with the darts per second
    ax2 = ax1.twinx()
    ax2.plot(n,dpsmp,'o--')
    ax2.hold(True)
    plt.ylabel('Simulation Rate (Darts/Second), dashed line')
    ax2.plot(n,dpsipy,'o--')
    ax2.plot(n,dpsserialr,'o--')
    #adjust the upper x limit so the final point is visible
    ax = plt.axis()
    nx = []
    nx.append(ax[0])
    nx.append(2E7)
    nx.append(ax[2])
    nx.append(ax[3])
    plt.axis(nx)
    #make the right axis label visible
    fig.subplots_adjust(right=0.85)
    plt.show()
    
