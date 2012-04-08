"""
AY250 Homework 4 Spring 2012 
Author: Cameron Bates
This script has functions to connect to a xmlrpc server and run image
manipulation methods on an image provided by the user. For each remote
method it runs the method saves the resulting image and then reconstructs
the original image and save a copy of that.
"""

import xmlrpclib
from matplotlib.pyplot import imread, imshow, show
import numpy as np
import Image
from scipy import ndimage
from scipy.misc import imsave

def buildimage(listimage):
    """
    function to unpack the serialized image back into the 
    standard python image formate ie. mxnx3 array
    """
    im = np.array(listimage[3:], dtype=np.uint8)
    im.shape = (listimage[1],listimage[2],listimage[0])
    return im 

def packimage(imagein):
    '''
    function to pack a standard RGB image to be sent to a remote server as a list.
    '''
    imagein = np.array(imagein)
    shape = np.shape(imagein)
    image = np.empty((3+np.size(imagein)))
    image[0] = shape[2]
    image[1] = shape[0]
    image[2] = shape[1]
    image[3:] = imagein.ravel()
    return image.tolist()

def remoterotate(imageinput,server):
    '''
    function to send an input RGB image to a remote server to be rotated and then
    rotate the image back and return the image to its original size and shape.
    '''
    inputshape = np.shape(imageinput)
    im = packimage(imageinput) 
    #send packed image to remote server   
    imrotate = server.rotateImage(im,45)
    im = buildimage(imrotate[1])
    #save rotated image
    imsave("rotatedimage.png",im)
    #unrotate and resize image back to its original size
    im = ndimage.rotate(im,-45)
    rotatedshape = np.shape(im)
    im = im[rotatedshape[0]/2-inputshape[0]/2:rotatedshape[0]/2+inputshape[0]/2\
    ,rotatedshape[1]/2-inputshape[1]/2:rotatedshape[1]/2+inputshape[1]/2,:]
    #save reconstructed image
    imsave("rotatedimagereconstruction.png",im)

def remoteinvert(imageinput,server):
    '''
    This function remotely inverts an input image using the input rpc server
    it then reconstructs the original image.
    '''
    im = packimage(imageinput)
    iminvert = server.invertImage(im)
    iminvert = buildimage(iminvert[1])
    imsave("invertedimage.png",iminvert)
    normal = 255-iminvert    
    imsave("invertedimagereconstruction.png",normal)
    
def remotecolorswap(imageinput,server):
    '''
    This function remotely swaps the color channels in an image and then
    swaps them back locally to reconstruct the image
    '''
    im = packimage(imageinput)
    imswap = server.swapColorChannels(im)
    imswap = buildimage(imswap[1])    
    tempimage = np.empty(np.shape(imswap), dtype=np.uint8)
    tempimage[:,:,0] = imswap[:,:,2]
    tempimage[:,:,1] = imswap[:,:,0]
    tempimage[:,:,2] = imswap[:,:,1]
    imsave("colorswapimage.png",imswap)
    imsave("colorswapimagereconstrution.png",tempimage) 
    
def runservermethods(imagefile,host,port):
    '''
    This function runs all three remote server test and reconstruction functions.
    It also opens the image and ensures that the color is in the correct format.
    '''
    server = xmlrpclib.ServerProxy("http://%s:%d" % (host, port))
    if ".png" not in imagefile:
        print "only .png files are supported at this time"
        return
    imin = Image.open(imagefile)
    imin = imin.convert(mode='RGB')    
    imsave('originalimage.png',imin)
    remotecolorswap(imin, server)
    remoteinvert(imin,server)
    remoterotate(imin,server)
    
if __name__ == '__main__':
    runservermethods('cat.png','ross-lbl.dhcp.lbl.gov',5010)    
    
