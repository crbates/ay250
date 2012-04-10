#Homework 9 AY 250 Spring 2012  
Author: Cameron Bates

Prior to running the hw9.py script start an ipython cluster with the desired
number of engines. This can be done using the command:  
ipcluster start -n 4  
This starts 4 engines. The output of running the script on a 2011 Macbook air
with a 1.8GHz dual-core processor with hyperthreading(4 effective threads) is
included in performanceplot.pdf. Running the hw9.py will produce the same 
output figure.  

Explanation of performance results:  
For small numbers of darts the overhead for the multiprocessing methods is much
larger than the improvement from splitting the task between multiple 
processors. That is the reason that below 10000 darts the serial code wins. As 
the number of darts increases, however, the overhead for the startup and 
communication to the other threads is small in comparison to the time doing 
computation. The mulitprocessing method has slightly lower overhead than the 
ipcluser method so it outperforms the ipcluster method at small sizes but as 
time spent doing computation becomes large they both reach about the same 
performance. At 1E6 darts thrown both the multiprocessing and ipcluster methods
are more or less completely computation bound. This can be seen by the fact the
the number of darts per second does not increase. It does not reach perfect 
scaling to the number of effective cores(4), this is most likely due to the 
overhead inherent in the parallelization schemes, system overhead, and the fact
that hyperthreading is not the same as having 4 independent cores.
