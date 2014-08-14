###############################################################################
##
## Copyright (C) 2014,
## All rights reserved.
## Contact: Dimas Rinarso <drp354@nyu.edu>
##
## This file is part of the Urban Computing Skills Lab, CUSP-GX-1000 assignments for students.
##
## "Redistribution and use in source and binary forms, with or without 
## modification, are permitted provided that the following conditions are met:
##
##  - Redistributions of source code must retain the above copyright notice, 
##    this list of conditions and the following disclaimer.
##  - Redistributions in binary form must reproduce the above copyright 
##    notice, this list of conditions and the following disclaimer in the 
##    documentation and/or other materials provided with the distribution.
##  - Neither the name of NYU-Poly nor the names of its 
##    contributors may be used to endorse or promote products derived from 
##    this software without specific prior written permission.
##
## THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" 
## AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, 
## THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR 
## PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR 
## CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, 
## EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, 
## PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; 
## OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, 
## WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR 
## OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF 
## ADVISED OF THE POSSIBILITY OF SUCH DAMAGE."
##
###############################################################################

import urllib2,json,argparse,sys,pyproj,shapefile 
import matplotlib.pyplot as m_plot
from matplotlib.path import Path
from matplotlib.patches import PathPatch
from matplotlib.ticker import MaxNLocator

def KeyCheck(key,line): 
  try:
      webUrl = urllib2.urlopen(urlData)
  except urllib2.HTTPError, e:
      print 'Failed with error code - %s.' % e.code
      if e.code == 403:
          sys.exit("API key incorrect. Please try again")
      sys.exit()
  
def WebAccess(key,line):
    # Open the URL and read the data
    webUrl = urllib2.urlopen(urlData)
    #print (webUrl.getcode())
    if (webUrl.getcode() == 200):
      data = webUrl.read()
      #print "Read data finished"
    else:
      sys.exit("Received an error from server, cannot retrieve results " + str(webUrl.getcode()))   
    return data
       
def printResults(data,busline):
  #declaration of local variables
  bus_num=0;
  pro=[];
  # Use the json module to load the string data into a dictionary
  theJSON = json.loads(data)  
  
  #Display bus line
  print "Bus Line               : "+busline
  
  #Display number of active buses
  for i in theJSON["Siri"]["ServiceDelivery"]["VehicleMonitoringDelivery"]:
    bus_num = len(i["VehicleActivity"])
  print "Number of Active Buses : "+str(bus_num)

  #Preparation for conversion
  proj=pyproj.Proj(init="esri:26918")
  print "Locations:\tLat/Long\t\t\t\t\tESRI:26918"
  #Storing coordinates of the buses
  for i in theJSON["Siri"]["ServiceDelivery"]["VehicleMonitoringDelivery"]:
    for j in i["VehicleActivity"]:
        lat=j["MonitoredVehicleJourney"]["VehicleLocation"]["Latitude"]
        lon=j["MonitoredVehicleJourney"]["VehicleLocation"]["Longitude"]
        pro.append(proj(lon,lat)) 
        print (lat,lon),"\t\t",proj(lon,lat)   
  return pro
 
            
def printMap(shpdir,outpdf,coord,line):
    #basic plot setting
    fig = m_plot.figure(figsize=(4.5, 7.2))
    fig.suptitle('Current '+line+' Bus Locations', fontsize=20)
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
    for i in xrange(len(coord)):
        ax.plot(coord[i][0],coord[i][1],'bo',markersize=6)
    
        ax.set_xlim(sf.bbox[0], sf.bbox[2])
    ax.set_ylim(sf.bbox[1], sf.bbox[3])
    ax.xaxis.set_major_locator(MaxNLocator(3))   

    fig.savefig(outpdf)
    print("Finished created : "+outpdf);

def main(bus_key,bus_line,shp_dir,out_pdf):
  #url data
  global urlData
  urlData = "http://api.prod.obanyc.com/api/siri/vehicle-monitoring.json?key="+bus_key+"&VehicleMonitoringDetailLevel=calls&LineRef="+bus_line
  
  #cheking API keys
  KeyCheck(bus_key,bus_line)
  
  # define a variable to hold the source URL
  data = WebAccess(bus_key,bus_line)
  
  #print the result
  global coord
  coord=printResults(data,bus_line)   
  
  #print the map
  printMap(shp_dir,out_pdf,coord,bus_line)
      
if __name__ == '__main__':
  parser = argparse.ArgumentParser()
  parser.add_argument("API_key", help="enter valid MTA API key")
  parser.add_argument("bus_line", help="enter the Bus Line ID")
  parser.add_argument("shp_dir", help="enter .shp file directory, e.g. nyc/SimplifiedStreetSegmentAnn.shp")
  parser.add_argument("output_pdf", help="enter output PDF name")
  args = parser.parse_args()
  key = args.API_key
  busline = args.bus_line
  shpdir = args.shp_dir
  outpdf = args.output_pdf
  main(key,busline,shpdir,outpdf)