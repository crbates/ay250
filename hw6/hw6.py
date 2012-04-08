'''
Homework 6 AY250 Spring 2012
Author: Cameron Bates
This script launches a pyQt gui contained within the class plotview. This gui can 
load images from the web and do masic actions on the images located in 
external functions. The gui uses a pool of processes to run things like image 
updates and image manipulation in a seperate thread. 

'''
import urllib2
import matplotlib
matplotlib.rcParams['backend.qt4']='PySide'
import PySide.QtCore as QtCore
import PySide.QtGui as QtGui
from hw6ui import Ui_MainWindow
import numpy as np
from qtmpl import MyMplCanvas
import scipy.ndimage as ndi
from skimage import filter as flt
from skimage import color
import string
import Image
import sys
import matplotlib.pyplot as plt
from multiprocessing import Pool


def rotateImage(image):
    '''
    function to rotate an image by 33 degrees
    '''
    return ndi.rotate(image, 33)

def blur(image):
    '''
    function that blurs an image using a gaussian filter with a width of 15
    '''
    return ndi.gaussian_filter(image,15)
        
def filterim(image):
    '''
    function that does edge detection on an image
    '''
    image = color.rgb2gray(image)
    image = np.array(flt.canny(image))        
    return image
    
def invert(image):
    '''
    takes input image (an RGB ndarray) and inverts it 
    '''
    return 255-image

def getimage(text):
    '''
    This function takes as input text that has the spaces removed and uses the 
    bing image search api to download the first search result. It then saves 
    the file and then loads it as an image into python using PIL. The image is 
    then converted into an RGB image and then a numpy array which is what is 
    returned.
    '''
    #run search query
    base1 = "http://api.bing.net/xml.aspx?AppId=55DD7D67CB5E72A490177D3C9850658014AED166&Query="
    base2 = "&Sources=Image&Version=2.0&Market=en-us&Adult=Moderate&Image.Count=1&Image.Offset=0"    
    infile = urllib2.urlopen(base1 +text + base2)
    test = infile.read()
    #determine image url
    section = test.split("<mms:MediaUrl>")[1]
    link = section.split("<")[0]
    imagetype = link.split(".")[-1]
    #save image    
    image = urllib2.urlopen(link)
    filename = 'temp.' + imagetype
    f = open(filename,'wb')
    f.write(image.read())
    f.close()
    #open image and return numpy array
    image = Image.open(filename)
    return (np.array(image.convert(mode='RGB')),link)


class plotview(QtGui.QMainWindow):
    '''
    This class instatiates the pyqt window in hw6ui.py and connects the signals
    of button pushes to image retrieval and editing functions. These functions
    are called asynchronously using the multiprocessing module so that the UI 
    is not affected.    
    '''
    def __init__(self, parent=None,cmdpipes = None):
        '''
        This initializes the UI and connects the buttons to functions. It also 
        starts a timer use to update the figure.
        '''
        #initialize window with matplotlib widget
        QtGui.QMainWindow.__init__(self, parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.pool = Pool(processes=1)
        self.result = None
        self.imageresult = None
        self.layout = QtGui.QVBoxLayout(self.ui.groupBox)
        self.figure = MyMplCanvas(self.ui.centralwidget, width=5, height=4, dpi=100)
        self.layout.addWidget(self.figure.canvas)
        self.layout.addWidget(self.figure.mpl_toolbar)
        #connect buttons to functions
        QtCore.QObject.connect(self.ui.searchbutton,QtCore.SIGNAL("clicked()"),self.get_image)
        QtCore.QObject.connect(self.ui.rotate,QtCore.SIGNAL("clicked()"),self.rotateImage_run)
        QtCore.QObject.connect(self.ui.blur,QtCore.SIGNAL("clicked()"),self.blur_run)
        QtCore.QObject.connect(self.ui.filter,QtCore.SIGNAL("clicked()"),self.filter_run)        
        QtCore.QObject.connect(self.ui.invert,QtCore.SIGNAL("clicked()"),self.invert_run)
        #setup and start figure update timer        
        self.timer = QtCore.QTimer(self)
        self.timer.start(250)
        QtCore.QObject.connect(self.timer, QtCore.SIGNAL("timeout()"), self.update_figure)      
        
    def update_figure(self):
        '''
        This function is called every 250 ms in order to update the displayed
        plot if necessary.
        '''
        #check if an image manipulation has returned and plot it
        if self.result is not None:
            if self.result.ready():
                self.image = self.result.get()
                if len( np.shape(self.image))>2:    
                     self.figure.axes.imshow(self.image)
                else:
                    self.figure.axes.imshow(self.image,cmap=plt.cm.gray)
                self.figure.canvas.draw()
                self.result = None
        #check if a search query has returned an image and plot it
        if self.imageresult is not None:
            if self.imageresult.ready():
                 self.image, link = self.imageresult.get()
                 self.ui.urllabel.setText(link)
                 if len( np.shape(self.image))>2:    
                     self.figure.axes.imshow(self.image)
                 else:
                    self.figure.axes.imshow(self.image,cmap=plt.cm.gray)
                 self.figure.canvas.draw()
                 self.imageresult = None
                 self.result = None

    def invert_run(self):
        #call invert image function asynchronously
        self.result = self.pool.apply_async(invert,(self.image,))

    def rotateImage_run(self):
        #call rotate image function asynchronously
        self.result = self.pool.apply_async(rotateImage,(self.image,))

    def blur_run(self):
        #call blur image function asynchronously
        self.result = self.pool.apply_async(blur,(self.image,))

    def filter_run(self):
        #call filter image function asynchronously
        self.result = self.pool.apply_async(filterim,(self.image,))

    def get_image(self):
        #get image based on text input 
        text = str(self.ui.search.text())
        text = string.replace(text,' ','')
        self.imageresult = self.pool.apply_async(getimage,(text,))


         
    
if __name__ == '__main__':
    '''
    This launches the window
    '''
    app = QtGui.QApplication(sys.argv)
    plot = plotview()
    plot.show()
    if app.exec_():
        pass
