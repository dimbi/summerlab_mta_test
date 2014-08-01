###############################################################################
##
## Copyright (C) 2014,
## All rights reserved.
## Contact: <drp354@nyu.edu>
##
## This file is part of the Urban Computing Skills Lab, CUSP-GX-1000.
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

import urllib2
import json
import argparse
import sys
import pyproj 

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
  bus_num=0;
  # Use the json module to load the string data into a dictionary
  theJSON = json.loads(data)  
  
  # Problem's answers
  #-------------------------------------
  #Display bus line
  print "Bus Line               : "+busline
  
  #Display number of active buses
  for i in theJSON["Siri"]["ServiceDelivery"]["VehicleMonitoringDelivery"]:
    for j in i["VehicleActivity"]:
        bus_num+=1
  print "Number of Active Buses : "+str(bus_num)

  #Preparation for conversion
  proj=pyproj.Proj(init="esri:26918")
  #Display bus locations
  print "Locations:\tLat/Long \t\t\t\t\t\t ESRI:26918"
  for i in theJSON["Siri"]["ServiceDelivery"]["VehicleMonitoringDelivery"]:
    for j in i["VehicleActivity"]:
        lat=j["MonitoredVehicleJourney"]["VehicleLocation"]["Latitude"]
        lon=j["MonitoredVehicleJourney"]["VehicleLocation"]["Longitude"]
        print (lat,lon),"\t\t\t",proj(lon,lat)
        
def main(bus_key,bus_line):
  #url data
  global urlData
  urlData = "http://api.prod.obanyc.com/api/siri/vehicle-monitoring.json?key="+bus_key+"&VehicleMonitoringDetailLevel=calls&LineRef="+bus_line
  #cheking API keys
  KeyCheck(bus_key,bus_line)
  # define a variable to hold the source URL
  data = WebAccess(bus_key,bus_line)
  #print the result
  printResults(data,bus_line)   
      
if __name__ == '__main__':
  parser = argparse.ArgumentParser()
  parser.add_argument("API_key", help="enter valid MTA API key")
  parser.add_argument("bus_line", help="enter the Bus Line ID")
  args = parser.parse_args()
  key = args.API_key
  busline = args.bus_line
  main(key,busline)