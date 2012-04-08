# -*- coding: utf-8 -*-
"""
Created on Tue Jan 31 20:11:41 2012
This plot recreates the figure stocks.png using google_data.txt, yahoo_data.txt,
and ny_temps.txt for part 2 of AY250 homework 1. 
@author: Cameron Bates
"""
from matplotlib.ticker import MultipleLocator

if __name__ == '__main__':
    import numpy as np
    import matplotlib.pyplot as plt
    
    # create data type and load data from all three text files
    googledt = np.dtype({'names':['MJD','Price'],'formats':['i4','f4']})
    googledata = np.loadtxt('google_data.txt',googledt)
    yahoodata = np.loadtxt('yahoo_data.txt',googledt)
    nydata = np.loadtxt('ny_temps.txt',googledt)
    fig = plt.figure(figsize =(16,12),dpi=210)
    #Create a subplot with the yahoo data and set hold to true
    ax = plt.subplot(111)
    plt.subplots_adjust(left = 0.075,top= 0.93)
    plt.plot(yahoodata['MJD'],yahoodata['Price'],color = '#9B30FF',label = 'Yahoo! Stock Value',linewidth = 3) 
    plt.hold(True)
       
    #add google stock data to te plot in purple
    plt.plot(googledata['MJD'],googledata['Price'],'b',label = 'Google Stock Value',linewidth = 3)      
    plt.ylim(-25,780)
    
    #add labels and title 
    fig.text(0.5,0.95,'New York Temperature, Google, and Yahoo!',weight = \
    'bold',size='36',family='serif',verticalalignment='bottom',\
    horizontalalignment= 'center')    
    plt.ylabel('Value(Dollars)',size='22')
    plt.xlabel('Date (MJD)',size='22')
    plt.tick_params(labelsize='18',length=14,width =3,pad=12)
    plt.tick_params(which='minor',labelsize='18',length=7,width =2,pad=12) 
    
    #turn on minor ticks and turn off ticks on top of the graph
    ml = MultipleLocator(20)
    ax.yaxis.set_minor_locator(ml)
    ax.xaxis.tick_bottom()

    #Add second axis with ny temperature data    
    ax2 = plt.twinx()
    plt.plot(nydata['MJD'],nydata['Price'],'r--',label= 'NY Mon. High Temp',linewidth = 3)
    plt.ylim(-150,100)
    plt.ylabel(u'Temperatue (\u00b0F)',size='22')
    plt.tick_params(labelsize='18',length=14,width =3,pad=12)
    plt.tick_params(which='minor',labelsize='16',length=7,width =2)    
    
    #make the axis spines thicker    
    for key in ax2.spines.keys():
        ax.spines[key].set_linewidth(2.5)
        
    #get labels from both axes and make a single legend
    handles, labels = ax.get_legend_handles_labels()
    handles2, labels2 = ax2.get_legend_handles_labels()
    handles.append(handles2[0])
    labels.append(labels2[0])    
    #format the legend location the line length and the font size
    plt.legend(handles,labels,bbox_to_anchor=(0.325,0.6),frameon=False,handlelength = 4 )
    leg = plt.gca().get_legend()
    ltext = leg.get_texts()    
    plt.setp(ltext, fontsize = '20')
    
    #turn on minor ticks and turn off ticks on top of the graph     
    ml = MultipleLocator(200)
    ax2.xaxis.set_minor_locator(ml)
    ax2.xaxis.tick_bottom()
    mls = MultipleLocator(10)
    ax2.yaxis.set_minor_locator(mls)
    
    #set x limit and save the figure
    plt.xlim(48800,55700)
    plt.savefig('stockscrb.png')
    