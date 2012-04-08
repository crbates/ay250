"""
Homework 4 AY250 Spring 2012
Author: Cameron Bates
This script determines which notes are in an input audio file using the base
frequencies found at : http://www.phy.mtu.edu/~suits/notefreqs.html. It does
this by taking the FFT of the signal multiplied by the Hann window, smoothing
it by convolving it with a gaussian and then finding significant peaks in that 
signal. It then compares the centroids of those peaks to known notes and
prints a list of the fundamental frequencies present. 
"""

import scikits.audiolab as al
import scipy.fftpack as fft
import matplotlib.pyplot as plt
import numpy as np
from scipy import signal

def findpeaks(audio,freqs):
    """
    This takes the fft of the audio as input along with the respective
    frequencies and finds the crude centroid of peaks above 15000. It
    returns a list of the centroid frequencies.
    """
    filtered =  audio > 15000
    inpeak = 0
    peaklist = []
    peakindexlist = []
    total = []
    for index,item in enumerate(filtered):
        if item == 1 and inpeak == 0:
            inpeak = 1
            peakindexlist = []
            total = []
        if item == 0 and inpeak == 1:
            inpeak = 0
            #calculate the centroid frequencies
            peaklist.append(sum(peakindexlist)/sum(total))
        if inpeak == 1:
            #append point to the current peak
            peakindexlist.append(audio[index]*freqs[index])
            total.append(audio[index])
      
    return peaklist      
        
            
def basefreq(audiofile):
    """
    This function reads in the audio file and does the hann windowed fft of 
    the right input. It then smooths the output using a gaussian filter and
    then finds the peaks. It returns the peaks in the right audio channel since
    testing showed there was no significant difference in the two.
    """
    #read the data into an ndarray using scikits-audiolab        
    data, rate, enc = al.aiffread(audiofile)
    #split the left and right channel
    datar = data[:,1]
    datal = data[:,0]
    #take the fft of both of the channels with the hann window applied
    #the hann window reduces spectral leakage in the FFT     
    dftr = abs(fft.fft(datar*signal.hann(len(datar))))
    dftl = abs(fft.fft(datal*signal.hann(len(datal))))
    #compute the frequencies in the FFT
    freq = float(rate)/float(len(datar))
    freqs = np.arange(len(dftr)/2+99)*freq
    dftr = dftr[0:np.size(dftr)/2]
    dftl = dftl[0:np.size(dftr)/2]
    #smooth the fft with a gaussian
    c = signal.gaussian(100,20)
    dftr = signal.convolve(dftr,c)
    dftl = signal.convolve(dftl,c)
    #find the significant peaks in each channel
    peaksr = findpeaks(dftr,freqs)
    peaksl = findpeaks(dftl,freqs)
    #plot the output fft for testing
    #plt.plot(freqs,dftr)
    #plt.show()
    #print peaksr
    return peaksr


def findfreq(audiofile):
    """
    This function finds the frequencies in the input aif audiofile. It does
    this by finding significant peaks in the FFT and then comparing those to
    known audio tones. It then prints out the frequencies found in the file.
    """
    peaks =  basefreq(audiofile)
    #print peaks
    #define all the base frequencies
    notes = { "c":[16.35,0],"csharp":[17.32,0],"d":[18.35,0],"dsharp":[19.45,0],\
    "e":[20.60,0],"f":[21.83,0],"fsharp":[23.12,0],"g":[24.50,0],"gsharp":[25.96,0],\
    "a":[27.5,0],"asharp":[29.14,0],"b":[30.87,0]}
    notesfound = []
    locations = []
    #iterate over the peaks in the fft
    for peak in peaks:
        found = 0
        #iterate over the frequencies
        for key in notes.keys():
            #check if the frequency is close to a multiple of a base frequency
            if abs(round(peak/notes[key][0])-peak/notes[key][0]) < 0.2 and notes[key][1] == 0:
                #determine whether it is also a harmonic ie. even power of 2
                for i in range(9):
                    if 2**i == round(peak/notes[key][0]):
                        #check if a note has already been found at the peak frequency
                        #if one has take use the closer one otherwise add the note to the list  
                        if found == 0:
                            notesfound.append("found: "+str(key)+str(i))
                            locations.append(abs(round(peak/notes[key][0])-peak/notes[key][0]))
                            #print "found: ",key,i
                            #print "at:", peak
                            notes[key][1] = 1
                            found = 1
                        if found == 1:
                            if abs(round(peak/notes[key][0])-peak/notes[key][0]) < locations[-1]:
                                locations[-1] = abs(round(peak/notes[key][0])-peak/notes[key][0])
                                notesfound[-1] = "found: "+str(key)+str(i)
    for item in notesfound:
        #print the notes found
        print item                        
                
if __name__ == '__main__':
    print "------------------------------"
    for i in range(1,13):
        print "file: sound_files/"+str(i)+'.aif:'
        findfreq("sound_files/"+str(i)+'.aif')
        print "------------------------------"




