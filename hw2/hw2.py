# -*- coding: utf-8 -*-
"""
AY250 Homework 2
@author: Cameron Bates
"""
import numpy as np
import scipy.stats
import math
import matplotlib.pyplot as plt

def rejectionsample(target,ref,samples):
    '''
    This function takes a target pdf that is a python function, a reference
    pdf that is a scipy.stats pdf(initialized if necessary), and the number of
    samples to return. It uses rejection sampling to sample the target pdf. It 
    returns a list of samples, the factor m and the accpetance ratio.
    '''
    r = scipy.stats.uniform(0,1)    
    m = 5
    n = 0
    #test values to determine m (Maxwell distribution is only defined for x>0)
    #all other distributions are symmetric around 0. 
    testx = np.linspace(0.1,10,100)
    testm = []    
    for item in testx:        
        testm.append(target(item)/ref.pdf(item))
    m = max(testm)
    result = []
    #find samples
    for i in range(samples):
        found = 0
        #This loop continues until an accepted sample is found
        while  found == 0:
            u = r.rvs()
            x = ref.rvs()
            n = n + 1
            #if the given sample satisfies these criteria accept it
            if u < target(x)/(m*ref.pdf(x)):
                result.append(x)
                found = 1
                
    return result, m , samples/float(n)


def laplace(x):
    '''
    This is a function to compute the laplace pdf
    '''
    return 1./2.*math.exp(-abs(x))
def submaxwell(x):
    '''
    This is a function to compute a maxwell like pdf
    '''
    return abs(x)*math.exp(-(x**2))*2    

    
if __name__ == '__main__':
    #This script does parts b-d
    
    #sample the laplace using the cauchy distribution
    r, m, acc = rejectionsample(laplace,scipy.stats.cauchy,1000) 
    print "Part b acceptance rate: ",acc
    #plot the sampled distribution and the actual laplace distribution    
    plt.hist(np.array(r),100,normed = True,label='samples')
    x = np.linspace(-10,10,1000)
    y = []
    for item in x:
        y.append(laplace(item))
    plt.hold(True)
    plt.plot(x,y,'r',label='laplace pdf')
    plt.ylabel("Density")
    plt.xlabel("x")
    plt.legend()
    plt.savefig('laplace.png')
    #determine the KS test distance
    d, p = scipy.stats.kstest(r,'laplace',loc =0,scale=1)
    print "KS test distance: ", d
    
    #instantiate students t test and repeat the sampling of the laplace distribution   
    t = scipy.stats.t(1,df=2)
    r2, m, acc2 = rejectionsample(laplace,t,1000) 
    print "Part c acceptance rate: ",acc2
    
    #sample my pdf using the maxwell boltzmann distribution
    r3, m3, acc3 =  rejectionsample(submaxwell,scipy.stats.maxwell,5000)
    
    #plot the sampled distribution in comparison with the actual one
    plt.hold(False)
    plt.hist(np.array(r3),100,normed = True,label='samples')
    plt.hold(True)
    x = np.linspace(0,10,1000)
    y = []
    for item in x:
        y.append(submaxwell(item))
    plt.plot(x,y,'r',label='my pdf')
    plt.legend()
    plt.ylabel("Density")
    plt.xlabel("x")
    plt.savefig('submaxwell.png')
