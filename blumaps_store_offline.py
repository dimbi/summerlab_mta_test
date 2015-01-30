###############################################################################
##
## blumaps_store_online.py
## fetch all bus data, simple plot and store it to postgre
## MTA bus key = 4723b4b0-3e16-4a17-a24b-48d79ea53dc0
##
###############################################################################

import urllib2,json,argparse,sys,pyproj,shapefile 
import matplotlib.pyplot as plt
from matplotlib.path import Path
from matplotlib.patches import PathPatch
from matplotlib.ticker import MaxNLocator
import time
import psycopg2
import psycopg2.extras
        
def storePostgre(dataDir, fileName):

  f = open(dataDir+"/"+fileName+"2014-08-01.txt")

 #connecting to postGres and write jsonData
  db = psycopg2.connect('dbname=json_test user=dimasrinarso password=bibirkubiasasaja')
  cur = db.cursor()

  #iterating each line from offline bus data  
  keyIdx = -1
  for line in f:
    tokenCount = -1
    keyIdx += 1
    line = line.strip()
    for tokens in line.split('\t'):
      tokenCount+=1
      if tokenCount == 0: 
        lat = tokens
      elif tokenCount == 1:
        lon = tokens
      elif tokenCount == 2:
        timeStamp = tokens
      elif tokenCount == 3:
        lineName = tokens
      elif tokenCount == 4:
        distancePerLine = tokens      
      elif tokenCount == 10:
        destName = tokens

  # Use the json module to load the string data into a dictionary
    cur.execute("INSERT INTO bus(id,time,line,destination,latitude,longitude,distance) VALUES (%s,%s,%s,%s,%s,%s,%s)",(keyIdx,timeStamp,lineName,destName,lat,lon, distancePerLine))
  db.commit()

def main():
  fileName = "MTA-Bus-Time_."
  offlineDir = "offline_data"   

  storePostgre(offlineDir,fileName)
      
if __name__ == '__main__':
  main()