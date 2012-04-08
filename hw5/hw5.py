"""
Cameron Bates AY250 homework 5
This is a set of functions to load the data provided from intrade about the republican
nomination, the republican VP nomination and the presidential election into a sqlite3
database. It provides tow functions to retrieve data from this database mdall and pall
mdall successively plots the probability of a candidate from north or south of the Mason
Dixon line winning the nomination for each race. pall plots the difference between the
the sum of all the probabilies that different candidates will win the election 
and 1. 

"""

import sqlite3
import urllib2
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import string
from os import listdir
from numpy import loadtxt
import datetime
from BeautifulSoup import BeautifulSoup as bs
import numpy as np

def getdata(name):
    '''
    This function takes a string in the format firstname_lastname and returns
    their city state party, birthday, and picture file location. It downloads a 
    picture of them if one exists on wikipedia in order to do this.
    '''
    
    #ambigous name cases
    if "Allen_West" in name:
        name = "Allen_West_(politician)"
    if "Jon_Huntsman" in name:
        name = "Jon_Huntsman,_Jr."
    if "John_Bolton" in name:
        name = "John_R._Bolton"
    
    #spoof the mozilla browser in order to get the page
    opener = urllib2.build_opener()
    opener.addheaders = [('User-agent', 'Mozilla/5.0')]
    print name
    infile = opener.open('http://en.wikipedia.org/w/index.php?title='+str(name)+"&printable=yes")
    page = infile.read()
    # parse the page using beautifulsoup and select the information box
    soup = bs(page)    
    res = soup.find(attrs={'class':'infobox vcard'})
    if res == None:
        res = soup.find(attrs={'class':'infobox biography vcard'})
    res = str( res)
    rows = string.split(res,"<tr")
    city = None
    state = None
    birthday = None
    party = None
    #iterate over the rows to find city, state, and party
    for row in rows:
        if "Born" in row:
            parts = row.split("<br")
            sections = parts[-1].split(",")            
            #print sections
            if "</a>" in sections[0]:
                city = sections[0].split("</a>")[0]
                city = city.split(">")[-1]
            else:
                city = sections[0].split("\n")[1]
            
            if len(sections) > 1:    
                if "</a>" in sections[1]:
                    state = sections[1].split("</a>")[0]
                    state = state.split(">")[-1]
                else:
                    state = sections[1]
            #print row        
            if ",_" in parts[-1]:
                city = sections[0].split("/")[-1]
                state = sections[1].split("\"")[0]
                state = state.lstrip("_")
                if len(state.split("_"))> 1:
                    state = state.split("_")[0] + " " + state.split("_")[1]
            #special cases for 3 candidates that don't use the stand formats        
            if "Giuliani" in name:
                city = "Brooklyn"
                state = "New York"
            if "Romney" in name:
                city = "Detroit"
                state = "Michigan"
            if "Trump" in name:
                city = "Queens"
                state = "New York"
            
        if "Political" in row and "party" in row :
            #print row
            data = string.split(row,'td')
 
            if not 'Donald_Trump' in name:
                #print data[1]
                if len(string.split(data[1],">"))>2:
                    #print data
                    data = string.split(data[1],"title=\"")[-1] 
                    #cases for candidates that don't use the standard format
                    if "United States Rep" in data:
                        party = "Republican"
                    else:    
                        party = string.split(data," ")[0]
                    if "New Progressive" in data:
                        party = "Republican"
                    if "Rick_Perry" in name:
                        party = "Republican"
            else:
                # special case for Donal Trump
                data = string.split(data[1],">")[1]
                party = string.split(data,"<")[0]

            #print party
            #party = string.split(row,"\"")[-2] 
    #use beautifulsoup to find the birth date
    soup = bs(res)
    bday = str(soup.find(attrs={'class':'bday'}))
    if not 'None' in bday:                 
        birthday = string.split(bday,'>')
        if len(birthday) > 1:
            birthday = string.split(birthday[1],"<")[0]
    
    #use beautifulsoup to find the image file
    soup = bs(res)
    images = str(soup.findAll('img'))
    
    #download the image file
    image = string.split(images,"src")
    if len(image) > 1:
        image = string.split(image[1],"\"")[1]
        imagetype = string.split(image,".")[-1]
        filename = 'pictures/' + name + '.' + imagetype
        if True:
            opener = urllib2.build_opener()
            opener.addheaders = [('User-agent', 'Mozilla/5.0')]
            infile = opener.open('http:'+image)            
            f = open(filename,'wb')
            f.write(infile.read())
            f.close()
    else:
        filename = None
        #This must be downloaded seperately because he doesn't have an imaage on wikipedia
        if "Roy_Moore" in name:
            opener = urllib2.build_opener()
            opener.addheaders = [('User-agent', 'Mozilla/5.0')]
            infile = opener.open("http://blog.al.com/breaking/2009/06/large_RoyMoore.JPG")
            filename = 'pictures/' + name + '.jpg'
            f = open(filename,'wb')
            f.write(infile.read())
            f.close()
            party = "Republican"
    #return data
    if "New York" in city:
        state = "New York"
        city = "New York"
    return city, state, party, birthday, filename
    

def initdb():
    '''
    This function creates the races table in the database and populates it. It also
    creates the elections.db sqlite database if it doesnt exist as well as calling
    functions to fill the candidates and prediction data tables.
    '''
    connection = sqlite3.connect("elections.db")
    cursor = connection.cursor()
    sql_cmd = """CREATE TABLE races (race_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT, election_date DATE, url TEXT)"""
    cursor.execute(sql_cmd)
    race_data = [('Republican Nomination',"11/4/12",'http://www.intrade.com/v4/markets/?eventId=84328'),
                 ('Presidential Election','11/4/12','http://www.intrade.com/v4/markets/?eventId=84326'),
                ('Republican VP Nominee','11/4/12','http://www.intrade.com/v4/markets/?eventId=90482')]
    for race in race_data:
        sql_cmd =  ("INSERT INTO races (name, election_date, url) VALUES " + str(race))
        cursor.execute(sql_cmd)
        
    
    #add candidate data to database
    parsecandidatewiki(cursor)
    #add prediction data to database
    connection.commit()        
    cursor.close()    
    loadpredictiondata()
    #save changes    
      
    
def parsecandidatewiki(cursor):    
    '''
    This creates the table of candidates in the database the is attached to the
    input cursor. It uses the filenames in the race_prediction_data folder.
    '''
    folder =  'race_prediction_data'   
    datafiles = listdir(folder)
    names = []
    sql_cmd = """CREATE TABLE candidates (candidate_id INTEGER PRIMARY KEY AUTOINCREMENT,
                                           name TEXT, city TEXT, state TEXT, party TEXT,
                                           birthday DATE, mdline INT, picture_file TEXT)"""
    cursor.execute(sql_cmd)
    for name in datafiles:
        firstname = name.split("_")[0]
        lastname = name.split("_")[1]
        name = firstname+"_"+lastname        
        if name not in names and "Any_other" not in name:
            names.append(name)
            city, state, party, birthday, filename = getdata(name)
            mdline = getlatitude(state)
            val = (name,city,state,party,birthday,mdline,filename)
            print val
            
            sql_cmd =  """INSERT INTO candidates(name, city, state, party, birthday,mdline, picture_file) values 
                        (?,?,?,?,?,?,?)"""
            cursor.execute(sql_cmd,val)

def getlatitude(state):
    '''
    This function uses the yahoo API to determine whether a location that is
    entered as a string is north or south of the mason dixon line.
    '''
    if state is not None:
        try:
            infile = urllib2.urlopen("http://where.yahooapis.com/geocode?q="+string.replace(state," ","_")+"&appid=CB84ju42")
            page = infile.read()
            soup = bs(page)    
            res = str(soup.latitude)
            res = res.split("latitude>")[1]
            res = res.split("</")[0]
            if float(res) > 39.722201:
                return 1
            else:
                return 0
        except:
            print "not a state: ", state
            return 0                                           
    else:
        return 0        
        
def loadpredictiondata():
    '''
    This function loads prediction data to the database elections.db from csv
    files located in the race_prediction_data folder.
    '''    
    connection = sqlite3.connect("elections.db")
    cursor = connection.cursor()
    sql_cmd = """CREATE TABLE predictions (id INTEGER PRIMARY KEY AUTOINCREMENT,
                                           candidate_id INTEGER, race_id INTEGER,
                                           date DATE, price FLOAT, volume FLOAT)"""
                                           
    cursor.execute(sql_cmd)
    folder =  'race_prediction_data'   
    datafiles = listdir(folder)
    for item in datafiles:
        #load data from csv file
        marketdata = loadtxt(folder+ '/' + item,skiprows=1,delimiter=',',
        dtype = 'S7,S7,float,float,float,float,float')
        firstname = item.split("_")[0]
        lastname = item.split("_")[1]
        if "RepNom" in item:
            race = '\"Republican Nomination\"'
        elif "RepVP" in item:
            race = '\"Republican VP Nominee\"'
        elif "Pres" in item:
            race = '\"Presidential Election\"'
        #determine race_id
        sql_cmd = """SELECT race_id FROM races where name like """ + str(race) 
        cursor.execute(sql_cmd)
        raceid = cursor.fetchall()
        #print raceid
        name = firstname+"_"+lastname
        #determine candidate_id
        sql_cmd = """SELECT candidate_id FROM candidates where name like """ + "\"" +str(name) + "\""
        cursor.execute(sql_cmd)
        candidateid = cursor.fetchall()
        #print candidateid
        if len(candidateid) > 0:            
            #insert data into database
            for row in marketdata:
                date = string.lstrip(row[0],'\"')
                year = string.rstrip(row[1],'\"')
                date = datetime.datetime.strptime(date+year,'%b %d %Y')            
                date = date.strftime('%Y-%m-%d')             
                price = row[-2]
                volume = row[-1]
                val = (candidateid[0][0],raceid[0][0],date,price,volume)
                sql_cmd =  """INSERT INTO predictions(candidate_id, race_id, date, price, volume) values 
                            (?,?,?,?,?)"""
                cursor.execute(sql_cmd,val)
    connection.commit()    
    cursor.close()
            
def plotmdline(md,rid):
    '''
    This function returns the sum of the probabilities of a candidate the is either
    north of the mason dixon line(md =1) or south of the mason dixon line (md =0)
    wins the race with the race id input (rid).
    '''
    
    #select data from the database
    connection = sqlite3.connect("elections.db")
    cursor = connection.cursor()
    sql_cmd = """SELECT predictions.date, predictions.price from predictions left join candidates on
    candidates.candidate_id = predictions.candidate_id where candidates.mdline=""" + str(md) + """ AND predictions.race_id="""+ str(rid) + """ ORDER BY predictions.date ASC"""
    cursor.execute(sql_cmd)
    result = cursor.fetchall()
    
    #sum the data for each date
    prevdate = result[0][0]
    dates = []
    price = []
    psum = 0    
    for item in result:
        if item[0] in prevdate:
            psum = psum + item[1]
        else:
            price.append(psum)
            psum = 0
            dates.append(item[0])
        prevdate = item[0]
    price.append(psum)
    #return the prices and dates
    return price, dates    
    #for item in result:

def comparemd(rid,name):
    '''
    This function compares the probability of a candidate from north of the mason
    dixon line winning to that of one south of the mason dixon line winning 
    normalized to one. the inputs are the race id (rid) and the name of the race.
    '''
    north, ndates = np.array(plotmdline(1,rid))#[0:1206]
    south, sdates = np.array(plotmdline(0,rid))
    ratio = []
    finaldates = []
    #compare when there is data for both on a given day    
    for index, date in enumerate(ndates):
        for index2, date2 in enumerate(sdates):
            if date == date2:
                if (north[index]+south[index2]) >0:
                    ratio.append(north[index]/(north[index]+south[index2]))
                else:
                    ratio.append(0)
                finaldates.append(datetime.datetime.strptime(date,"%Y-%m-%d"))
       
    #Plot a figure of the two probabilities
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.plot(finaldates,ratio,label='North wins ' + name)
    plt.hold(True)
    ax.plot(finaldates,1-np.array(ratio),label='South wins ' + name)
    plt.xlabel("Date")
    plt.ylabel("probability of winning")
    plt.legend(loc=2)
    plt.hold(False)
    fig.autofmt_xdate()
    plt.show()
                
def mdall():
    '''
    This function plots the probability of a candidate from north or south of
    the mason dixon line winning for all the races in the races table.
    '''
    connection = sqlite3.connect("elections.db")
    cursor = connection.cursor()
    sql_cmd = "SELECT race_id, name FROM races"
    cursor.execute(sql_cmd)
    result = cursor.fetchall()
    for item in result:
        comparemd(item[0],item[1])
def pall():
    '''
    This function plots the difference between the sum of the probabilities of 
    a republican or Barack Obama winning in comparison to 1.    
    '''
    #This gets data for republican candidates
    connection = sqlite3.connect("elections.db")
    cursor = connection.cursor()
    sql_cmd = """SELECT predictions.date, predictions.price from predictions left join candidates on
    candidates.candidate_id = predictions.candidate_id where predictions.race_id=2 and candidates.party like \"Republican\" ORDER BY predictions.date ASC"""
    cursor.execute(sql_cmd)            
    result = cursor.fetchall()
    #Sum all the data for each date    
    prevdate = result[0][0]
    dates = []
    price = []
    psum = 0     
    for item in result:
        if item[0] in prevdate:
            psum = psum + item[1]
        else:
            price.append(psum)
            psum = 0
            dates.append(item[0])
        prevdate = item[0]
    price.append(psum)
    #Get the prediction data for Barack Obama
    sql_cmd = """SELECT predictions.date, predictions.price from predictions left join candidates on
    candidates.candidate_id = predictions.candidate_id where predictions.race_id=2 and candidates.name like \"Barack_Obama\" ORDER BY predictions.date ASC"""
    cursor.execute(sql_cmd)            
    result = cursor.fetchall()
    dprice = []
    ddates = []
    total = []
    finaldates = []
    for item in result:
        dprice.append(item[1])
        ddates.append(item[0])
    #sum the probabilities for all shared dates    
    for index, date in enumerate(dates):
        for index2, date2 in enumerate(ddates):
            if date == date2:
                total.append(100-(price[index]+dprice[index2]))
                finaldates.append(datetime.datetime.strptime(date,"%Y-%m-%d"))
    #plot the result
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.plot(finaldates,total)
    yearsFmt = mdates.DateFormatter('%m-%d-%Y')
    ax.xaxis.set_major_formatter(yearsFmt)
    fig.autofmt_xdate()
    plt.xlabel("Date")
    plt.ylabel("Total probability deficit (%)")
    plt.show()

def selectcandidatedata(results):
    # select the information for the candidate of interest     
    connection = sqlite3.connect("elections.db")
    cursor = connection.cursor()
    sql_cmd = """SELECT predictions.date, predictions.price from predictions left join candidates on
        candidates.candidate_id = predictions.candidate_id where predictions.race_id=""" + str(results.race) + """ and
        candidates.name like \"%""" + str(results.candidate) + """%\" ORDER BY predictions.date ASC"""
    cursor.execute(sql_cmd)            
    result = cursor.fetchall()
    dprice = []
    ddates = []
    #iterate over the requested data to find the requested date
    for item in result:
        dprice.append(item[1])
        ddates.append(item[0])
        #print item[0]
        if item[0] in results.date:
            price = item[1]
            print "Candidate: ", results.candidate, " Date: ", item[0], " probability: ", item[1], "%" 
    return dprice, ddates, price

def plotprobability(dprice,ddates,results, price):
    #change the dates to datetime objects for plotting
    finaldates = []
    for date in ddates:
        finaldates.append(datetime.datetime.strptime(date,"%Y-%m-%d"))
    #plot the result
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.plot(finaldates,dprice)
    yearsFmt = mdates.DateFormatter('%m-%d-%Y')
    ax.xaxis.set_major_formatter(yearsFmt)
    fig.autofmt_xdate()
    plt.hold(True)
    plt.plot(datetime.datetime.strptime(results.date,"%Y-%m-%d"),price,'ro')
    plt.xlabel("Date")
    plt.ylabel("Probability of winning (%)")
    plt.show()
