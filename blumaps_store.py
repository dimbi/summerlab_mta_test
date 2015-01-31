###############################################################################
##
## blumaps_sample.py
## fetch all bus data, simple plot and store it to postgre
## MTA bus key = 4723b4b0-3e16-4a17-a24b-48d79ea53dc0
## contact: drp354@nyu.edu
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


def KeyCheck(): 
  try:
      webUrl = urllib2.urlopen(urlData)
  except urllib2.HTTPError, e:
      print 'Failed with error code - %s.' % e.code
      if e.code == 403:
          sys.exit("API key incorrect. Please try again")
      sys.exit()
  
def WebAccess():
    # Open the URL and read the data
    webUrl = urllib2.urlopen(urlData)
    #print (webUrl.getcode())
    if (webUrl.getcode() == 200):
      data = webUrl.read()
      #print "Read data finished"
    else:
      sys.exit("Received an error from server, cannot retrieve results " + str(webUrl.getcode()))   
    return data
        
def storePostgre(pgData):

  # Use the json module to load the string data into a dictionary
  jsonData = json.loads(pgData)  

  #connecting to postGres and write jsonData
  db = psycopg2.connect('dbname=json_test user=dimasrinarso password=bibirkubiasasaja')
  cur = db.cursor()

  #Preparation for conversion
  keyIdx = -1
  for i in jsonData["Siri"]["ServiceDelivery"]["VehicleMonitoringDelivery"]:
    for j in i["VehicleActivity"]:
      keyIdx += 1
      lineName=j["MonitoredVehicleJourney"]["PublishedLineName"]
      destName=j["MonitoredVehicleJourney"]["DestinationName"]
      lat=j["MonitoredVehicleJourney"]["VehicleLocation"]["Latitude"]
      lon=j["MonitoredVehicleJourney"]["VehicleLocation"]["Longitude"]
      timeStamp=j["RecordedAtTime"]
      print keyIdx
      cur.execute("INSERT INTO bus(id,time,line,destination,latitude,longitude) VALUES (%s,%s,%s,%s,%s,%s)",(keyIdx,timeStamp,lineName,destName,lat,lon))
  db.commit()

def main(bus_key,shp_dir,out_pdf):

  #url data
  global urlData
  urlData = "http://api.prod.obanyc.com/api/siri/vehicle-monitoring.json?key="+bus_key

  #cheking API keys
  KeyCheck()
  
  # define a variable to hold the source URL
  data = WebAccess()
 
  storePostgre(data)

  #print the result
  #global coord
  #coord=printResults(data)   
  
  #print the map
  #rintMap(shp_dir,out_pdf,coord)


      
if __name__ == '__main__':
  key = "4723b4b0-3e16-4a17-a24b-48d79ea53dc0"
  shpdir = "./nyc/SimplifiedStreetSegmentAnn.shp"
  outpdf = "output.pdf"
  main(key,shpdir,outpdf)
