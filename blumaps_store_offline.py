###############################################################################
##
## blumaps_store_online.py
## fetch all bus data, simple plot and store it to postgre
## MTA bus key = 4723b4b0-3e16-4a17-a24b-48d79ea53dc0
## contact: drp354@nyu.edu
##
###############################################################################

import argparse
import time
import psycopg2
import psycopg2.extras
from datetime import date,datetime,timedelta

#global init
start_date='2014-08-01'
end_date='2014-10-31'
startDate = datetime.strptime(start_date,"%Y-%m-%d")
endDate = datetime.strptime(end_date,"%Y-%m-%d")

def daterange(startDate, endDate):
  for n in range(int ((endDate - startDate).days)):
    yield startDate + timedelta(n)

  
notInList = ["2014-10-06","2014-10-17"]
      
def storePostgre(dataDir, fileName):

  #iterating each line from offline bus data  
  keyIdx = -1
  
  for singleDate in daterange(startDate, endDate):
    if (singleDate.strftime("%Y-%m-%d")) in notInList: pass

    #debug only
    #if (singleDate.strftime("%Y-%m-%d")) == "2014-08-02":
    #    break

    else:
      #open each data
      f = open(dataDir+"/"+fileName+(singleDate.strftime("%Y-%m-%d"))+".txt")

      #connecting to postGres and write jsonData
      db = psycopg2.connect('dbname=bus_data user=postgres password=postgres')
      cur = db.cursor()

      tempCounter = -1
      headerIdx = -1
      for line in f:
        tempCounter+=1
        tokenCount = -1
        keyIdx += 1
        headerIdx += 1
        if headerIdx == 0:
          pass
        else:
          line = line.strip()
          for tokens in line.split('\t'):
            tokenCount+=1
            if tokenCount == 0: 
              lat = tokens
            elif tokenCount == 1:
              lon = tokens
            elif tokenCount == 2:
              timeStamp = tokens
            elif tokenCount == 7:
              lineName = tokens      
            elif tokenCount == 10:
              destName = tokens

          # Use the json module to load the string data into a dictionary
          cur.execute("INSERT INTO bus(id,timestamp,line,destination,latitude,longitude) \
                       VALUES (%s,%s,%s,%s,%s,%s)",
                      (keyIdx,timeStamp,lineName,destName,lat,lon))

          #For debug purpose only
          #if tempCounter==10:
          #  break
 
      db.commit()
      print "data on date "+(singleDate.strftime("%Y-%m-%d"))+" inserted successfully."

def main():
  fileName = "MTA-Bus-Time_."
  offlineDir = "offline_data"   

  storePostgre(offlineDir,fileName)
      
if __name__ == '__main__':
  main()
