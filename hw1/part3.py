# -*- coding: utf-8 -*-
"""
Created on Tue Jan 31 21:22:36 2012
This is part 3 of homework 1 for AY250. This shows 4 plots in a window. If 
the user selects a subset of the data by left-clicking and dragging over 
the data in the lower right plot the corresponding data in the other plots 
will be turned red. The rectangles can be deleted by mousing over the 
rectangle and clicking the d button.

@author: cameron bates
"""
import matplotlib.pyplot as plt
import matplotlib
import numpy as np

class rectangle():
    '''
    This class holds the matplotlib rectangle object and related information
    '''
    xp = 0
    yp = 0
    xc = 0
    yc = 0
    rect = None
    indices = []
    live = 1
    dead = 0
    left = -1E9
    right = 1E9
    top = 1E9
    bottom = -1E9

class mplwidget():
    '''
    This class creates a matplotlib figure with 4 subplots. The plot in the 
    lower left corner can have sub areas selected using a rectangle. This
    rectangle can be deleted using the d key with the mouse over the 
    rectangle. There is no limit to the number of rectangles that can be 
    selected.
    '''
    def __init__(self):
        '''
        This initializes the figure with 4 plots and connects the matplotlib
        events to the methods in this class.
        '''
        self.box = 0
        self.fig = plt.figure()                
        self.canvas = self.fig.canvas
        self.canvas.mpl_connect('motion_notify_event', self.on_motion)             
        self.canvas.mpl_connect('button_press_event', self.on_press)
        self.canvas.mpl_connect('button_release_event', self.on_release)
        self.canvas.mpl_connect('key_press_event', self.key_press)
        self.fitpoint = 0
        points = 100
        self.pressed = 0
        self.x = np.random.normal(12,9,points)
        self.y = np.random.normal(18,12,points)
        self.z = np.random.normal(7,5,points)
        self.s = np.random.normal(3,2,points)
        self.rectangles = []
        self.ax = self.fig.add_subplot(221)
        self.ax.scatter(self.x,self.y)
        self.ax2 = self.fig.add_subplot(222)
        self.ax2.scatter(self.x,self.z)
        self.ax3 = self.fig.add_subplot(223)
        self.ax3.scatter(self.y,self.z)
        self.ax4 = self.fig.add_subplot(224)
        self.ax4.scatter(self.x,self.s)
        self.drawlabels()
        plt.title("Multi-dimensional data brushing")
        plt.show()
        
    def drawlabels(self):
        '''
        This draws x and y labels on all of the graphs
        '''
        self.ax4.set_xlabel('x')
        self.ax4.set_ylabel('s')
        self.ax3.set_xlabel('y')
        self.ax3.set_ylabel('z')
        self.ax2.set_xlabel('x')
        self.ax2.set_ylabel('z')
        self.ax.set_xlabel('x')
        self.ax.set_ylabel('y')        
        
    def key_press(self,event):
        '''
        This method deletes a rectangle if the d key is pressed and the mouse
        is in the rectangle. It will delete all rectangles under the mouse 
        pointer.
        '''
        if 'd' in event.key:
            for i in range(len(self.rectangles)):
                if event.xdata > self.rectangles[i].left and event.xdata < self.rectangles[i].right:
                    if event.ydata > self.rectangles[i].bottom and event.ydata < self.rectangles[i].top:
                        if self.rectangles[i].dead == 0:                        
                            self.rectangles[i].indices = []
                            if self.rectangles[i].rect is not None:
                                self.rectangles[i].rect.remove()
                            # this keeps a rectangle that has already been
                            #deleted from being removed again    
                            self.rectangles[i].dead = 1
            #redraw the plots with the rectangle and associated highlighted points removed            
            self.colorpoints(self.ax,self.x,self.y)
            self.colorpoints(self.ax2,self.x,self.z)
            self.colorpoints(self.ax3,self.y,self.z)
            self.canvas.draw()
    
    def on_press(self,event):
        '''
        This adds a rectangle object when the mouse is pressed and makes it 
        live(editable).
        '''
        if event.inaxes == self.ax4:
            self.pressed = 1
            rect = rectangle()
            rect.xp = event.xdata
            rect.yp = event.ydata
            rect.live = 1
            self.rectangles.append(rect)    
            
    def getpoints(self,x,y):
        '''
        This adds the indices of the points inside the currently live 
        rectangle to the list of indices to highlight. 
        '''
        for i, r in enumerate(self.rectangles):
            if r.live == 1:
                self.rectangles[i].indices = []
                for index, point in enumerate(x):
                    if point > self.rectangles[i].left and point < self.rectangles[i].right:
                        if y[index] > self.rectangles[i].bottom and y[index] < self.rectangles[i].top:
                            self.rectangles[i].indices.append(index)

    def colorpoints(self,ax,x,y):
        '''
        This iterates through the rectangles and changes the color of the 
        points that are located within rectangles. 
        '''
        normalx = []
        normaly = []
        selectedx = []
        selectedy = []
        
        #split points into selected and non-selected groups
        for r in self.rectangles:
            for index, point in enumerate(x):
                if index in r.indices:
                    selectedx.append(x[index])
                    selectedy.append(y[index])
                else:
                    normalx.append(x[index])
                    normaly.append(y[index])
                    
        #if there are selected points plot them in red            
        if len(selectedy) >0:        
            ax.hold(False)
            ax.scatter(normalx,normaly)
            ax.hold(True)
            ax.scatter(selectedx,selectedy,c='r')
            self.drawlabels()
        else:
            ax.hold(False)
            ax.scatter(x,y)
            self.drawlabels()
                
            
    def on_motion(self,event):
        '''
        This updates the currently live rectangle and the associated colored
        points in the other subplots when the mouse is moved and the mouse
        button is clicked. It only works in the bottom right plot.
        '''
        if self.pressed == 1:
            for i in range(len(self.rectangles)):
                if self.rectangles[i].live == 1:
                    self.rectangles[i].xc = event.xdata
                    self.rectangles[i].yc = event.ydata
                    
                    #Determine limits of rectangle
                    if self.rectangles[i].xc >= self.rectangles[i].xp:
                        self.rectangles[i].left = self.rectangles[i].xp
                        self.rectangles[i].right = self.rectangles[i].xc
                        self.rectangles[i].width = self.rectangles[i].xc - self.rectangles[i].xp
                    else:
                        self.rectangles[i].left = self.rectangles[i].xc
                        self.rectangles[i].right = self.rectangles[i].xp
                        self.rectangles[i].width = self.rectangles[i].xp - self.rectangles[i].xc
                    if self.rectangles[i].yc >= self.rectangles[i].yp:
                        self.rectangles[i].bottom = self.rectangles[i].yp
                        self.rectangles[i].top = self.rectangles[i].yc
                        self.rectangles[i].height = self.rectangles[i].yc - self.rectangles[i].yp 
                    else:
                        self.rectangles[i].bottom = self.rectangles[i].yc
                        self.rectangles[i].top = self.rectangles[i].yp
                        self.rectangles[i].height = self.rectangles[i].yp - self.rectangles[i].yc
                    #remove old rectangle                    
                    if self.rectangles[i].rect is not None:                       
                        self.rectangles[i].rect.remove()
                        self.rectangles[i].rect =  None
                    #update list of highlighted points    
                    self.getpoints(self.x,self.s)
                    #draw highlighted points
                    self.colorpoints(self.ax,self.x,self.y)
                    self.colorpoints(self.ax2,self.x,self.z)
                    self.colorpoints(self.ax3,self.y,self.z)
                    #draw rectangle and add it to the axes                        
                    self.rectangles[i].rect = matplotlib.patches.Rectangle((self.rectangles[i].left,\
                    self.rectangles[i].bottom),self.rectangles[i].width,self.rectangles[i].height,fill=False)                                                                                             
                    event.inaxes.add_patch(self.rectangles[i].rect) 
                    self.canvas.draw()              
                
                    
    def on_release(self,event):
        '''
        This makes the currently live rectangle no longer editable by setting
        live to 0 when the mouse button is released.
        '''
        self.pressed = 0
        for index, r in enumerate(self.rectangles):
            if r.live == 1:
                self.rectangles[index].live = 0

if __name__ == '__main__':
    '''
    This simply instantiates the class
    '''
    main = mplwidget()
    
    


