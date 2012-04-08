#!/usr/bin/env python
"""
AY 250 Spring 2012
Homework Assignment 3 - Parallel Feature Extraction Example
Author: Cameron Bates
Original Author: Christopher Klein
This code is an extension of the parallel feature extraction code written by
Chris. The function classifydata takes a folder and categories images in the subfolder into 
50 catgories and prints the results to results.txt. In addition this code has functions
to compare performance of different features using a kfolds cross validation test. 
It can also extract features from training data using run_training_classifier that
are then saved for later use.
"""
from os import listdir
from skimage import color
from skimage import filter as flt
from multiprocessing import Pool, cpu_count
from matplotlib.pylab import imread
from scipy import ndimage
import numpy as np
from time import time
from sklearn.ensemble import RandomForestClassifier
from sklearn import cross_validation

def reduceimages(image_paths):
    '''
    This function takes returns 1/10th of the images for testing purposes
    '''
    res = []
    for index, path in enumerate(image_paths):
        if index % 10 == 0:
            res.append(path)
    return res
        

def split_seq(seq, size):
    '''
    Quick function to divide up a large list into multiple small lists, 
    attempting to keep them all the same size. 
    '''
    newseq = []
    splitsize = 1.0/size*len(seq)
    for i in range(size):         
        newseq.append(seq[int(round(i*splitsize)): int(round((i+1)*splitsize))])
    return newseq


def extract_features(image_path_list):
    '''
    This function takes a list of image paths and computes several features of each 
    image in order to classify them. This include both basic properties like size 
    and aspect ratio as well as doing object recognition and counting. This runs at
    about 1/s/core on a quad-core with HT 2.93 GHz i7.
    '''
    feature_list = []
    name_list = []
    file_list = []
    #iterate through all the image paths
    for image_path in image_path_list:
        image_array = imread(image_path)
        feature = []
        feature.append(image_array.size)
        shape = image_array.shape
        #check if the image isblack or white 
        if len(shape) > 2:
            feature.append(1)
            #convert color images to grey so they can be compared with greyscale ones
            image_array = color.rgb2grey(image_array)
            '''
            # Can't use these because there is nothing comparable for black and
            # white images
            feature.append(sum(sum(image_array[:,:,0])))        
            feature.append(sum(sum(image_array[:,:,1])))
            feature.append(sum(sum(image_array[:,:,2])))
            hsv = color.rgb2hsv(img_as_float(image_array))              
            feature.append(sum(sum(hsv[:,:,0])))        
            feature.append(sum(sum(hsv[:,:,1])))        
            feature.append(sum(sum(hsv[:,:,2])))
            '''
        else:
            feature.append(0)
            #print "bw: ", image_path
        #determine basic image shape properties
        feature.append(shape[0])
        feature.append(shape[1])
        feature.append(shape[0]/shape[1])
        #compute the amount of different shades of grey and their ratios
        black = np.average(image_array.flat <= 0.25 )
        darkgrey = np.average((image_array.flat > 0.25) & (image_array.flat <= 0.5))
        lightgrey = np.average((image_array.flat > 0.5) & (image_array.flat <= 0.75)) 
        white = np.average(image_array.flat > 0.75)
        feature.append(black)
        feature.append(darkgrey)
        feature.append(lightgrey)
        feature.append(white)
        feature.append(black/(white+1))
        feature.append(lightgrey/(darkgrey+1))
        feature.append(lightgrey/(black+1))
        
        # compute the average of several common filter outputs
        feature.append(np.average(flt.sobel(image_array)))
        feature.append(np.average(ndimage.morphological_gradient(image_array, size=(2,2))))
        feature.append(np.average(flt.prewitt(image_array)))
        feature.append(np.average(flt.canny(image_array)))
        
        #Use the canny filter to delineate object and then count the objects and 
        #their average size
        p = flt.canny(image_array)
        #plt.imshow(p,cmap=plt.cm.gray,interpolation='nearest')
        #plt.show()
        labels, count = ndimage.label(p)
        area = np.sum((labels>0))/count        
        feature.append(area)
        feature.append(count)
        
        #determine the filename for the results file and the image type for the 
        #training set.
        filename = image_path.split("/")[-1]
        file_list.append(filename)
        image = filename.split('_')[0]        
        name_list.append(image)        
        feature_list.append(feature)
    return name_list, feature_list, file_list

def run_training_classifier(path):
    '''
    This function runs the feature extractor on the images in the subdirectories of 
    this input path and saves the result to the numpy object trainingdata.npy. It
    uses as many processors as are available. 
    '''
    image_paths = []
    categories = listdir(path)
    for category in categories:
        image_names = listdir(path + category)
        for name in image_names:
            image_paths.append(path + category + "/" + name)
    
    print ("There should be 4244 images, actual number is " + 
        str(len(image_paths)) + ".")
    
    # Then, we run the feature extraction function using multiprocessing.Pool so 
    # so that we can parallelize the process and run it much faster.
    numprocessors = cpu_count() # To see results of parallelizing, set numprocessors
                                # to less than cpu_count().
    # numprocessors = 1
    #print numprocessors
    #quit()
    # We have to cut up the image_paths list into the number of processes we want to
    # run. 
    #image_paths = reduceimages(image_paths)
    split_image_paths = split_seq(image_paths, numprocessors)
        
    # Ok, this block is where the parallel code runs. We time it so we can get a 
    # feel for the speed up.
    
    #extract_features(split_image_paths[0])
    #quit()
    start_time = time()
    p = Pool(numprocessors)
    result = p.map_async(extract_features, split_image_paths)
    result.wait()
    poolresult = result.get()
    end_time = time()
    
    # All done, print timing results.
    print ("Finished extracting features. Total time: " + 
        str(round(end_time-start_time, 3)) + " s, or " + 
        str( round( (end_time-start_time)/len(image_paths), 5 ) ) + " s/image.")
    # This took about 10-11 seconds on my 2.2 GHz, Core i7 MacBook Pro. It may also
    # be affected by hard disk read speeds.
    
    # To tidy-up a bit, we loop through the poolresult to create a final list of
    # the feature extraction results for all images.
    combined_result = []
    for single_proc_result in poolresult:
        for single_image_result in single_proc_result:
            combined_result.append(single_image_result)
    
    np.save('trainingdata',combined_result)
    
def classifydata(path):
    '''
    This function takes a path with images and classifies it using the 
    trainingdata.npy dataset. It first extracts the features of all the images and
    then uses a random forest classifier trained on the training.npy dataset to
    predict the class of each image. It then writes the predictions to an output 
    file called results.txt.
    '''

    #This determines the file names in the folder and extracts the features from them
    image_paths = []
    image_dir = listdir(path)    
    for name in image_dir:
            image_paths.append(path + "/" + name)    
    numprocessors = cpu_count() 
    split_image_paths = split_seq(image_paths, numprocessors)
    p = Pool(numprocessors)
    result = p.map_async(extract_features, split_image_paths)
    result.wait()
    poolresult = result.get()
    combined_result = []
    for single_proc_result in poolresult:
        for single_image_result in single_proc_result:
            combined_result.append(single_image_result)
    combined_result = fixdata(combined_result)
    
    #This part loads the training data and then runs the classifier on it and then 
    #predicts the category of each of the input images. Finally it writes this to a 
    #text file
    trainingdata = np.load('trainingdata.npy')
    trainingdata = fixdata(trainingdata)
    data = np.array(trainingdata[1])
    target = np.array(trainingdata[0])    
    un, inv = np.unique(target,return_inverse=True)
    clf = RandomForestClassifier(n_estimators=100)
    clf = clf.fit(data,inv)
    filenames = combined_result[2]
    result = clf.predict(combined_result[1])
    output = open('results.txt','w')
    output.write('filename \t predicted_class\n')
    output.write('-------------------------------\n') 
    for index, item in enumerate(result):
        output.write(filenames[index]+ "\t" + un[item] +'\n')

def getscore(combined_result,i= None,All = False):
    '''
    This function uses the cross validation score module in scikits-learn to
    determine the classification accuracy. It can use all the feautures, remove one
    to test its importance or remove all to see how well random guessing would work.
    It returns the mean of the score of 5 kfolds based cross validation tests.
    '''
    data = np.array(combined_result[1])
    if i is not None:    
        data[:,i] = 1
    if All:
        data[:,:] = 1
    target = np.array(combined_result[0])    
    un, inv = np.unique(target,return_inverse=True)
    clf = RandomForestClassifier(n_estimators=100)
    clf = clf.fit(data,inv)
    scores = cross_validation.cross_val_score(clf, data, inv, cv=5,n_jobs=-1)
    return scores.mean()

def analyze_scores():
    '''
    This function determines the relative importance of each of the features by 
    removing one at a time and comparing the performance to using all of the 
    features. 
    '''
    combined_result = fixdata()
    #print out a baseline score
    combinedscore = getscore(combined_result)
    print combinedscore
    #print out the score if no features were used (random guessing)
    guessing = getscore(combined_result,All = True)
    print guessing
    #quit()
    scorediff = []
    data = np.array(combined_result[1])
    #print data
    #loop over all features and compare performance with the feature removed
    for i in range(len(data[0,:])):
        scorediff.append(combinedscore-getscore(combined_result,i))
    scorediff = np.array(scorediff)
    #create an indexed array and sort on the difference to determine the most
    #important features
    dtype = [('index',int),('value',float)]    
    stack = np.zeros((18,),dtype)
    for i in range(18):
        stack[i] = i, scorediff[i]
    print np.sort(stack,order='value')

def fixdata(combined_result =None):
    '''
    This function takes data from the training classifier that is incorrectly 
    formatted and rearranges it from:
        0,1,2,3,4,5...
    to:
        [[0,3,6...],[1,4,7...],[2,5,8...]]
        
    '''
    if combined_result is None:
        combined_result = np.load('trainingdata.npy')
    for i in range(0,len(combined_result),3):
        if i == 0:
            names = np.array(combined_result[i])
            features = np.array(combined_result[i+1])
            files = np.array(combined_result[i+2])
        else:
            #print i
            #print names.shape
            #print combined_result[i].shape
            names = np.concatenate((names,combined_result[i]))
            features = np.concatenate((features,combined_result[i+1]))
            files = np.concatenate((files,combined_result[i+2]))

    return names, features, files
    
if __name__ == '__main__':
    '''
    This script can be run along with one of the commented out functions below to either
    create a new training set or classify data. 
    '''
    pass
    #run_training_classifier('50_categories/')     
    #classifydata('50_categories/killer-whale')   