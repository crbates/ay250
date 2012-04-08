#Homework 8 AY250 Spring 2012  
Author: Cameron Bates

## Part 1
The changelog.txt file contains the commit log from a project I recently started.

## Part 2
The github repository can be found [here](https://github.com/crbates/ay250)

## Part 3
The hw8.py file in this folder can be run with the following arguments:  
  -c CANDIDATE  Candidates name default:Obama  
  -d DATE       Date in yyyy-mm-dd format default:2012-03-14  
  -r RACE       race id 1: Republican Nomination 2:Presidential Election 3:Republican VP default:2  
  -p            plot results  
  -i            initialize database  

The database should already be ready assuming elections.db has not been deleted. In case it has been deleted the -i flag can be used to run the database initialization routines from the homework 5 folder. Two functions  were added to the hw5.py file(selectcandidatedata and plotprobability) to retrieve the requested data from the database and plot it.

