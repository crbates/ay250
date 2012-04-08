# -*- coding: utf-8 -*-
"""
Created on Tue Jan 31 18:56:50 2012
This reproduces a plot previously made in excel in matplotlib for part 1 of
AY250 homework 1.
@author: cameron bates
"""
if __name__ == '__main__':
    import sys
    import matplotlib
    sys.path.append('../../libraries/generic')
    #This is a parser to turn the .spe file into something useful
    from maestrofile import maestrofile
    data = maestrofile('Background_ROI.Spe')
    #plot the data and set the xlimits and labels
    matplotlib.pyplot.semilogy(data.energy,data.counts)
    matplotlib.pyplot.xlim(2000,3200)    
    matplotlib.pyplot.xlabel('Energy(keV)')
    matplotlib.pyplot.ylabel('Counts')    
    #add anotations for the two energies of interest
    matplotlib.pyplot.annotate('Tl 208-2614 keV', xy=(2614, 10000),  xycoords='data',
                    xytext=(-80, 30), textcoords='offset points',
                    arrowprops=dict(arrowstyle="->",
                    connectionstyle="arc,angleA=0,armA=30,rad=10"),
                    )
    matplotlib.pyplot.annotate('Tl 208 SE 2102.73 keV', xy=(2102, 1000),  xycoords='data',
                    xytext=(-20, 45), textcoords='offset points',
                    arrowprops=dict(arrowstyle="->",
                    connectionstyle="arc,angleA=0,armA=0,rad=10"),
                    )
    
    
    #after this points all pyplot commands will default to the second axes
    ax2 = matplotlib.pyplot.twiny()
    #adds the raw channel number of the digitizer to the plot
    matplotlib.pyplot.xlabel('Channel Number')
    matplotlib.pyplot.xlim(10171,16171)
    #display the plot(plot saved using the interactive figure saving feature)  
    matplotlib.pyplot.show()

