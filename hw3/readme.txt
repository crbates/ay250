AY250 HW3 Spring 2012 read me
Author: Cameron Bates

files:
trainingdata.npy: numpy dataset that contains the extracted features from the 50_categories dataset
hw3.py :This contains the script to classify data using the numpy dataset.

The script can be run on a folder by uncommenting the classifydata function and correcting the folder name.

This classifier is ~ 16.3% better than random guessing using the k-folds cross validation method.

The most important features are:
1. amount of "white" in the image 
2. image width in pixels
3. average feature area

These were computed by setting one feature at a time to 1 and then comparing the new cross validation score. The differences were small most likely due to many of the features being closely correlated.
