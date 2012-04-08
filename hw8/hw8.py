import sys
import argparse
#This adds the parent directory to the path which includes hw5
sys.path.append("../")
import hw5.hw5

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
    
dprice, ddates, price = hw5.hw5.selectcandidatedata(results)

#check if a plot it requested    
if results.plot:
    hw5.hw5.plotprobability(dprice,ddates,results, price)    
