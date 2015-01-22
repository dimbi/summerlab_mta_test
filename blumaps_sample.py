###############################################################################
##
## blumaps_sample.py
## fetch all bus data, simple plot and store it to postgre
## MTA bus key = INSERT
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
       
def printResults(data):
  #declaration of local variables
  pro=[];
  # Use the json module to load the string data into a dictionary
  busJson = json.loads(data)  

  #Preparation for conversion
  proj=pyproj.Proj(init="esri:26918")
  for i in busJson["Siri"]["ServiceDelivery"]["VehicleMonitoringDelivery"]:
    for j in i["VehicleActivity"]:
        lat=j["MonitoredVehicleJourney"]["VehicleLocation"]["Latitude"]
        lon=j["MonitoredVehicleJourney"]["VehicleLocation"]["Longitude"]
        pro.append(proj(lon,lat)) 

  storePostgre(busJson)
  return pro
 
def storePostgre(jsonData):
  #hardcode
  keyIdx = 10
  #connecting to postGres and write jsonData
  #try:
  db = psycopg2.connect('dbname=json_test user=dimasrinarso password=bibirkubiasasaja')
  cur = db.cursor()
  cur.execute("INSERT INTO bus(id,data) VALUES (%s,%s)",(keyIdx,json.dumps(jsonData)))
  db.commit()

  #except psycopg2.Error as e:
  #  sys.exit("Error when connecting or writing to postGres database = %s : %s", (e.pgcode,e.pgerror))
      
def printMap(shpdir,outpdf,coord):

    #basic plot setting
    fig = plt.figure(figsize=(4.5, 7.2))
    fig.suptitle('Current Bus Locations', fontsize=20)
    ax = fig.add_subplot(111, aspect='equal')
    
    #read .shp file
    sf = shapefile.Reader(shpdir)
    
    #iterating through each records
    for sr in sf.shapeRecords():
        color = '0.8'
        if sr.record[1]!='      ':
            color='orange'
            
        parts = list(sr.shape.parts) + [-1]
            
        for i in xrange(len(sr.shape.parts)):
            path = Path(sr.shape.points[parts[i]:parts[i+1]])
            patch = PathPatch(path, edgecolor=color, facecolor='none', lw=0.5, aa=True)
            ax.add_patch(patch)
    
    #plot the bus projection coordinates onto the rendered maps
    #matplotlib interactive mode 
    #plt.ion()
    #plotting points

    #infinite repetition
    #while True:
    for i in xrange(len(coord)):
        ax.plot(coord[i][0],coord[i][1],'bo',markersize=6)
        ax.set_xlim(sf.bbox[0], sf.bbox[2])
    ax.set_ylim(sf.bbox[1], sf.bbox[3])
    ax.xaxis.set_major_locator(MaxNLocator(3))   

    plt.show()

    #sleep 5 secs
    #time.sleep(5)

    #DEBUG: printing to PDF
    #fig.savefig(outpdf)
    #print("Finished created : "+outpdf);


def main(bus_key,shp_dir,out_pdf):

  #url data
  global urlData
  urlData = "http://api.prod.obanyc.com/api/siri/vehicle-monitoring.json?key="+bus_key+"&VehicleMonitoringDetailLevel=calls"
  
  #cheking API keys
  KeyCheck()
  
  # define a variable to hold the source URL
  data = WebAccess()
  
  #print the result
  global coord
  coord=printResults(data)   
  
  #print the map
  printMap(shp_dir,out_pdf,coord)


      
if __name__ == '__main__':
  key = "PUT YOUR API KEY HERE"
  shpdir = "../nyc/SimplifiedStreetSegmentAnn.shp"
  outpdf = "output.pdf"
  main(key,shpdir,outpdf)
