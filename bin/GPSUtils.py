
# DONE: Create class to handle GPS data retrieving and processing
# TODO: - getData() -> string
# DONE: - translateGPStoImage(string) -> (float x, float y)
# TODO: - translateImagetoGPS(float x, float y) -> string
# DONE: - calculate linear regression in __init__ to provide the translation matrix
# TODO: - getAlt() -> float
# TODO: - getLat() -> float 
# TODO: - getLong() -> float

import os
from gps import *
from time import *
import time
import threading

import numpy as np
from pyproj import Proj, CRS, transform

gpsd = None #seting the global variable
 
os.system('clear') #clear the terminal
 
class GpsUtils(threading.Thread):
  
  longitudesWS84 = [-2.7233336,
-3.4400004,
-1.6436111,
-4.1677778,
-2.3786112,
-0.7427778,
-3.6641666,
-2.9233333,
-1.7322223,
-2.1033335,
-4.4216667,
-5.0636111,
-2.8566667,
-0.3850000,
-2.0800000,
-3.8166664,
-1.4058333,
-0.5947223,
-3.4719445,
-0.1447222,
-0.4500000, 
-1.5047223,
-1.4752778]
  latitudesWS84 = [47.7191667,
47.7605556,
47.7916667,
47.9750000,
48.0019444,
48.0322222,
48.0536111,
48.0569444, 
48.0719444,
48.4433333, 
48.4472222,
48.4633333,
48.5375000,
48.5447222,
48.5877778,
48.6008333,
48.6608333,
48.7497222,
48.7544444, 
48.9269444,
49.1733333,
49.2033333, 
49.6508333]
  
  longitudesRGF93 = None
  latitudesRGF93 = None

  longitudespixels = [4025, 2961, 5650, 1919, 4584, 7023, 2682, 3782, 5555, 5057, 1639, 699, 3961, 7604, 5112, 2561, 6114, 7317, 3095, 7993, 7570, 6038, 6136]
  latitudespixels = [7979, 7806, 7925, 7237, 7390, 7463, 7129, 7209, 7297, 6437, 6156, 6030, 6152, 6350, 6120, 5898, 6017, 5880, 5601, 5516, 4949, 4804, 3812]

  def __init__(self):
    threading.Thread.__init__(self)
    global gpsd #bring it in scope
    gpsd = gps(mode=WATCH_ENABLE) #starting the stream of info
    self.current_value = None
    self.running = True #setting the thread running to true
    longitudesRGF93, latitudesRGF93 = self.transformation(self.latitudesWS84, self.longitudesWS84)

  def run(self):
    global gpsd
    while self.running:
      gpsd.next() #this will continue to loop and grab EACH set of gpsd info to clear the buffer

  def transformation(latitudesWS84, longitudesWS84):
    crs = CRS.from_proj4("+proj=lcc +lat_1=49 +lat_2=44 +lat_0=46.5 +lon_0=3 +x_0=700000 +y_0=6600000 +ellps=GRS80 +towgs84=0,0,0,0,0,0,0 +units=m +no_defs ")
    inProj = Proj('epsg:4326')
    outProj = Proj(crs)
    longitudesRGF93, latitudesRGF93 = transform(inProj, outProj, latitudesWS84, longitudesWS84)
    return longitudesRGF93, latitudesRGF93
  
  def interpolation(self, longitudeRGF93, latitudeRGF93):
      unknown_longPi = np.interp(longitudeRGF93, self.longitudesRGF93, self.longitudespixels) 
      unknown_latPi = np.interp(latitudeRGF93, self.latitudesRGF93, self.latitudespixels)
      return unknown_longPi, unknown_latPi

if __name__ == '__main__':
  gpsp = GpsUtils() # create the thread
  try:
    gpsp.start() # start it up
    while True:
      #It may take a second or two to get good data
      #print gpsd.fix.latitude,', ',gpsd.fix.longitude,'  Time: ',gpsd.utc
 
      os.system('clear')
      #print
      #print (' GPS reading')
      #print ('----------------------------------------')
      #print ('latitude    ' , gpsd.fix.latitude)
      #print ('longitude   ' , gpsd.fix.longitude)
      #print ('time utc    ' , gpsd.utc,' + ', gpsd.fix.time)
      #print ('altitude (m)' , gpsd.fix.altitude)
      #print ('eps         ' , gpsd.fix.eps)
      #print ('epx         ' , gpsd.fix.epx)
      #print ('epv         ' , gpsd.fix.epv)
      #print ('ept         ' , gpsd.fix.ept)
      #print ('speed (m/s) ' , gpsd.fix.speed)
      #print ('climb       ' , gpsd.fix.climb)
      #print ('track       ' , gpsd.fix.track)
      #print ('mode        ' , gpsd.fix.mode)
      #print
      #print ('sats        ' , gpsd.satellites)
      time.sleep(5) #set to whatever

  except (KeyboardInterrupt, SystemExit): #when you press ctrl+c
    print ("\nKilling Thread...")
    gpsp.running = False
    gpsp.join() # wait for the thread to finish what it's doing
  print ("Done.\nExiting.")