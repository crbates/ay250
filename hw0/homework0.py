# -*- coding: utf-8 -*-
"""
Created on Mon Jan 23 15:57:10 2012

@author: cameron bates 
@email: cameron.r.bates at gmail.com
"""
import string
import numpy
import urllib
import networkx
import matplotlib.pyplot

class bearland():
    '''
    This class holds all functions and objects to simulate a bear population
    as defined by AY250 spring 2012 homework 0.  
    '''
    def __init__(self):
        '''
        This method initializes all the variables along with the 3 starting
        bears: Adam, Eve, and Mary.
        '''
        self.network = networkx.DiGraph()
        self.bears = []
        self.bearsborn = 0        
        self.year = 0
        self.addbear('Adam ',sex = 'male')
        self.addbear('Eve ',sex = 'female')
        self.addbear('Mary ',sex = 'female')
        self.name = self.getname()
                
        
    def getname(self):
        '''
        This method retrieves the top 1000 boy names from the year 2010 and yields
        names based on a concatenation of 2 randomly chosen names from the list.
        '''
        data = urllib.urlencode({'year':'2010','top':'1000'})
        urlreq = urllib.urlopen("http://www.ssa.gov/cgi-bin/popularnames.cgi",data).read()
        lines = string.split(urlreq,'\n')    
        readout  = 0
        namelist = []
        for line in lines:
            if readout == 1:
                if '<td>' in line:
                    data = line.split('<td>')
                    data = data[2].split('</td>')[0]    
                    namelist.append(data)
            if 'Popularity for top 1000'  in line:
                readout = 1
        namefound  = False
        names = []
        while 1:
            i1, i2, i3 = numpy.random.rand(3)*1000
            name = namelist[int(i1)] + " " + namelist[int(i2)] 
            namefound = True
            if name in names:
                namefound = False
            if namefound:
                names.append(name)
                yield name
      
    def getlifetime(self):
        '''
        This function returns the lifetime of a given bear
        based on a normal distribution with mean 35 and 
        standard deviation of 5.
        '''
        return numpy.random.normal(35,5,1)[0]
        
    def addbear(self,name = None,mother=None,father = None,sex = None):
        '''
        This method adds new bears to the population held in the dictionary 
        self.bears with a name, lifetime, mother, father, and sex. The name,
        lifetime and sex are chosen randomly.
        '''
        self.bearsborn = self.bearsborn + 1
        if name is None:        
            name = self.name.next()
            
        lifetime = self.getlifetime()
        
        #determine the sex a given probability(normally 0.5)
        if sex is None:
            if numpy.random.rand(1) > 0.5:
                sex = 'male'
            else:
                sex = 'female'
                
        #add nodes to network        
        self.network.add_node(name)
        if mother is not None:
            self.network.add_edge(mother,name)
        if father is not None:
            self.network.add_edge(father,name)
        self.bears.append({'name':name,'mother':mother,'father':father,\
        'lifetime':lifetime,'age':0,'sex':sex,'timesincemating':0})
        
    def agebears(self):
        '''
        This method ages the bears by one year and removes bears who
        are older than their lifespan.
        '''
        self.year = self.year + 1
        deadbears = []
        for index, bear  in enumerate(self.bears):
            bear['age'] = bear['age'] + 1
            bear['timesincemating'] = bear['timesincemating'] + 1            
            if bear['age'] > bear['lifetime']:
                deadbears.append(index)
        n = 0
        #remove dead bears from the population                
        for bear in deadbears:
            self.bears.pop(bear-n)
            n = n + 1
            
    def matebears(self):
        '''
        This method mates all the bears and adds bears to the population. It
        iterates over all the males and females in the population and finds
        pairs of bears that follow the selection rules for being able to mate. 
        '''                
        for index1, female in enumerate(self.bears):
            if 'female' in female['sex'] and female['timesincemating'] > 4:
                matenotfound = True            
                for index2, male in enumerate(self.bears): 
                    if matenotfound and 'male' == male['sex'] and \
                    male['timesincemating'] > 4 and abs(male['age']-female['age']) < 10:
                        if male['mother'] is None and female['mother'] is None:
                            matenotfound = False
                            self.addbear(mother=female['name'],father = male['name'])
                            self.bears[index1]['timesincemating'] = 0
                            self.bears[index2]['timesincemating'] = 0
                        elif  male['mother'] != female['mother'] and male['father'] != female['father']:
                            matenotfound = False
                            self.addbear(mother=female['name'],father = male['name'])
                            self.bears[index1]['timesincemating'] = 0
                            self.bears[index2]['timesincemating'] = 0
                    if not matenotfound:
                        break
                    
def findparents(graph,name,pregraph):
    '''
    This method recursively finds the parents of a bear with a given name. It 
    then builds a networkx graph of all the bear's predecessors.
    '''
    if len(graph.predecessors(name)) > 0:
        pred = graph.predecessors(name)
        pregraph.add_edge(pred[0],name)
        pregraph.add_edge(pred[1],name)
        findparents(graph,pred[0],pregraph)
        findparents(graph,pred[1],pregraph)

def runsim(years):
    '''
    This script simulates the bear population for the number of years input saving the 
    population after each year. It also creates a network map of the 
    ancestors of the last bear and plots it.    
    '''
    sim = bearland()
    pop = []
    while sim.year < years:
        if sim.year % 10 == 0:
            print sim.year
        sim.agebears()
        if sim.year % 5 == 0:
            sim.matebears()
        #numpy.save('bears',sim.bears)
        pop.append(len(sim.bears))
    if len(sim.bears) > 0:
        pregraph = networkx.DiGraph()
        findparents(sim.network,sim.bears[-1]['name'],pregraph)
        pos=networkx.graphviz_layout(pregraph,prog='dot',args='')
        networkx.draw(pregraph,pos)
        matplotlib.pyplot.show()
        numpy.save('pop',pop)    
    sim.name.close()
    return sim           
                            
    
                
