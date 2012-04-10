'''
Homework 9
Author: Cameron Bates

'''

from time import time
from multiprocessing import cpu_count

def serial(number_of_darts):
    from random import uniform
    from math import sqrt
    number_of_darts_in_circle = 0
    for n in range(number_of_darts):
        x, y = uniform(0,1), uniform(0,1)
        if sqrt((x - 0.5)**2 + (y - 0.5)**2) <= 0.5:
            number_of_darts_in_circle += 1
    return number_of_darts_in_circle

def serialpi(number_of_darts):
    start = time()
    serial(number_of_darts)
    stop = time()
    return stop-start

def calcdartspp(nproc,ndarts):
    dpp = []
    mod = ndarts % nproc
    rough = ndarts/nproc
    while ndarts != mod:
        ndarts -= rough
        dpp.append(rough)
    dpp[-1] += mod
    return dpp  

def multiprocessingpi(number_of_darts):    
    from multiprocessing import Pool  
    final = 0
    nproc = cpu_count()
    p = Pool(nproc)
    start = time()
    dartspp = calcdartspp(nproc,number_of_darts)
    result = p.map_async(serial,dartspp)
    result.wait()
    poolresult = result.get()
    for item in poolresult:
        final += item
    stop = time()
    
    #print 4*final/float(number_of_darts) 
    return stop-start

def ipcluster(number_of_darts):
    from IPython.parallel import Client
    c = Client() 
    final = 0
    nproc = len(c.ids)
    start = time()
    dartspp = calcdartspp(nproc,number_of_darts)
    #print dartspp
    result = c[:].map_sync(serial,dartspp)
    for item in result:
        final += item
    stop = time()
    return stop-start

if __name__ == '__main__':
    import numpy as np
    n = [25,50,300,1000,5000,20000,100000,1000000]#np.logspace(2,7,8)
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
    dpsmp = np.array(n)/mp
    dpsipy = np.array(n)/ipy
    dpsserialr = np.array(n)/serialr
    
    fig = plt.figure()
    ax1 = fig.add_subplot(111)
    plt.plot(n,mp,'o-',label='multiprocessing')
    plt.hold(True)
    plt.plot(n,ipy,'o-',label='ipcluster')
    plt.loglog(n,serialr,'o-',label='serial')
    plt.xlabel('Number of Darts Thrown')
    plt.ylabel('Execution Time (Seconds), solid line')
    plt.legend(loc=2)
    
    ax2 = ax1.twinx()
    ax2.plot(n,dpsmp,'o--')
    ax2.hold(True)
    plt.ylabel('Simulation Rate (Darts/Second), dashed line')
    ax2.plot(n,dpsipy,'o--')
    ax2.plot(n,dpsserialr,'o--')
    ax = plt.axis()
    nx = []
    nx.append(ax[0])
    nx.append(2E6)
    nx.append(ax[2])
    nx.append(ax[3])
    plt.axis(nx)
    fig.subplots_adjust(right=0.85)
    plt.show()
    
