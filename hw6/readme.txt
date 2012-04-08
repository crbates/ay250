Homework 6 AY250 Spring 2012
Author: Cameron Bates

In order to run this homework it is necessary to have pyQt installed. It can 
be downloaded here: http://www.riverbankcomputing.co.uk/software/pyqt/download
It also uses the latest stable version of scikits-image (0.5). 

The main file is hw6.py that laods the ui and contains all the image retrieval 
and processing functions. The file qtmpl.py contains a simple matplotlib widget
that can be inserted into a PyQt ui. The file hw6.ui contains the qt designer
xml file that describes the user interface. The file hw6ui.py contains the 
result of running pyuic4 hw6.ui > hw6ui.py. 

Running the hw6.py file will launch a window that allows one to enter a query
for an image and display the result as well as edit the result using the 
provided functions. This is done asynchronously so the ui is still responsive
when buttons are pressed. One other note is that the ok button is connected
to the window closing button in the hw6.ui file. 
