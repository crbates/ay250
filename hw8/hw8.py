import sys
import argparse
#This adds the parent directory to the path which includes hw5
sys.path.append("../")
import hw5.hw5
import sqlite3
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import datetime

#argument parsing setup
parser = argparse.ArgumentParser(description='intrade election data')
parser.add_argument('-c',dest='candidate',help='Candidates name default:Obama',default='Obama')
parser.add_argument('-d',dest='date',help='Date in yyyy-mm-dd format default:2012-03-14',default='2012-03-14')
parser.add_argument('-r',dest='race',help='race id 1: Republican Nomination 2:Presidential Election 3:Republican VP default:2',default=2)
parser.add_argument('-p',action='store_true',dest='plot',help='plot results')
parser.add_argument('-i',action='store_true',dest='init',help='initialize database')
results = parser.parse_args()

#initializes the database if requested
if results.init:
    hw5.hw5.initdb()
    
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
total = []
finaldates = []
#iterate over the requested data to find the requested date
for item in result:
    dprice.append(item[1])
    ddates.append(item[0])
    #print item[0]
    if item[0] in results.date:
        price = item[1]
        print "Candidate: ", results.candidate, " Date: ", item[0], " probability: ", item[1], "%"

#check if a plot it requested    
if results.plot:
    #change the dates to datetime objects for plotting
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
