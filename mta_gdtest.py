import urllib2
import json
import argparse
import sys

def KeyCheck(key,line): 
  urlData = "http://api.prod.obanyc.com/api/siri/vehicle-monitoring.json?key="+key+"&VehicleMonitoringDetailLevel=calls&LineRef="+line
  try:
      webUrl = urllib2.urlopen(urlData)
  except urllib2.HTTPError, e:
      print 'Failed with error code - %s.' % e.code
      if e.code == 403:
          sys.exit("API key incorrect. Please try again")
      sys.exit()
  
def WebAccess(key,line):
    urlData = "http://api.prod.obanyc.com/api/siri/vehicle-monitoring.json?key="+key+"&VehicleMonitoringDetailLevel=calls&LineRef="+line
 
    # Open the URL and read the data
    webUrl = urllib2.urlopen(urlData)
    if (webUrl.getcode() == 200):
      data = webUrl.read()
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

  #Display bus locations
  print "Locations              :  Lat/Long"
  for i in theJSON["Siri"]["ServiceDelivery"]["VehicleMonitoringDelivery"]:
    for j in i["VehicleActivity"]:
        print j["MonitoredVehicleJourney"]["VehicleLocation"]["Latitude"],j["MonitoredVehicleJourney"]["VehicleLocation"]["Longitude"]
        
def main(bus_key,bus_line):
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
