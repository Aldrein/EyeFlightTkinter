
# DONE: Create class to handle GPS data retrieving and processing
# TODO: - getData() -> string
# DONE: - translateGPStoImage(string) -> (float x, float y)
# TODO: - translateImagetoGPS(float x, float y) -> string
# DONE: - calculate linear regression in __init__ to provide the translation matrix
# TODO: - getAlt() -> float
# TODO: - getLat() -> float 
# TODO: - getLong() -> float

from cmath import pi, sin, cos, sqrt, log, tan, exp
import gpsd

import numpy as np

class GpsUtils():

  longitudesWS84 = [-0.5, -0.5, -0.5, -0.5, -0.5, -0.5, -0.5, -1, -1, -1, -1, -1, -1, -1, -1.5, -1.5, -1.5, -1.5, -1.5, -1.5, -1.5, -2, -2, -2, -2, -2, -2, -2, -2.5, -2.5, -2.5, -2.5, -2.5, -2.5, -2.5, -3, -3, -3, -3, -3, -3, -3, -3.5, -3.5, -3.5, -3.5, -3.5, -3.5, -3.5, -4, -4, -4, -4, -4, -4.5, -4.5, -4.5, -4.5, -4.5, -5, -5, -5, -5, -5]
  latitudesWS84 = [51, 50.5, 50, 49.5, 49, 48.5, 48, 51, 50.5, 50, 49.5, 49, 48.5, 48, 51, 50.5, 50, 49.5, 49, 48.5, 48, 51, 50.5, 50, 49.5, 49, 48.5, 48, 51, 50.5, 50, 49.5, 49, 48.5, 48, 51, 50.5, 50, 49.5, 49, 48.5, 48, 51, 50.5, 50, 49.5, 49, 48.5, 48, 50, 49.5, 49, 48.5, 48, 50, 49.5, 49, 48.5, 48, 50, 49.5, 49, 48.5, 48]
  #longitudesWS84 = [-2.7233336, -3.4400004, -1.6436111, -4.1677778, -2.3786112, -0.7427778, -3.6641666, -2.9233333, -1.7322223, -2.1033335, -4.4216667, -5.0636111, -2.8566667, -0.3850000, -2.0800000, -3.8166664, -1.4058333, -0.5947223, -3.4719445, -0.1447222, -0.4500000, -1.5047223, -1.4752778]
  #latitudesWS84 = [47.7191667, 47.7605556, 47.7916667, 47.9750000, 48.0019444, 48.0322222, 48.0536111, 48.0569444, 48.0719444, 48.4433333, 48.4472222, 48.4633333, 48.5375000, 48.5447222, 48.5877778, 48.6008333, 48.6608333, 48.7497222, 48.7544444, 48.9269444, 49.1733333, 49.2033333, 49.6508333]
  
  longitudesRGF93 = []
  latitudesRGF93 = []

  longitudespixels = [7677, 7627, 7578, 7529, 7480, 7430, 7381, 6974, 6917, 6861, 6805, 6748, 6692, 6635, 6272, 6208, 6145, 6082, 6018, 5955, 5891, 5570, 5499, 5429, 5358, 5288, 5217, 5147, 4868, 4790, 4712, 4635, 4557, 4480, 4403, 4166, 4081, 3996, 3912, 3828, 3743, 3659, 3465, 3373, 3821, 3190, 3099, 3007, 2916, 2566, 2468, 2369, 2271, 2172, 1852, 1746, 1641, 1535, 1430, 1138, 1025, 912, 800, 688]
  latitudespixels = [880, 1994, 3106, 4218, 5330, 6441, 7551, 847, 1960, 3073, 4184, 5295, 6405, 7515, 810, 1922, 3034, 4145, 5255, 6366, 7475, 767, 1880, 2990, 4102, 5212, 6321, 7430, 720, 1832, 2943, 4053, 5163, 6272, 7381, 669, 1780, 2891, 4001, 5110, 6218, 7327, 613, 1724, 2834, 3943, 5052, 6160, 7267, 2773, 3881, 4989, 6097, 7204, 2707, 3815, 4922, 6029, 7135, 2637, 3744, 4851, 5957, 7062]
  #longitudespixels = [4025, 2961, 5650, 1919, 4584, 7023, 2682, 3782, 5555, 5057, 1639, 699, 3961, 7604, 5112, 2561, 6114, 7317, 3095, 7993, 7570, 6038, 6136]
  #latitudespixels = [7979, 7806, 7925, 7237, 7390, 7463, 7129, 7209, 7297, 6437, 6156, 6030, 6152, 6350, 6120, 5898, 6017, 5880, 5601, 5516, 4949, 4804, 3812]

  a = 6378137       #demi-grand axe de l'éllipsoïde (m)
  e = 0.08181919106 #première exentricité à l'origine
  x0 = 700000       #coordonnées à l'origine
  y0 = 6600000      #coordonnées à l'origine
  echelle = 50      #mètres/pixel

  def init(self):
    while True:
      gpsd.connect()
      packet = gpsd.get_current()
      if packet.mode < 2:
        break
    
    for i in range(len(self.longitudesWS84)):
      longRGF93, latRGF93 = self.conversionWS84toRGF93(self.longitudesWS84[i], self.latitudesWS84[i])
      self.longitudesRGF93.append(longRGF93)
      self.latitudesRGF93.append(latRGF93)

    print("LenghtWS84 = ", len(self.longitudesWS84)," ; LenghtRGF = ", len(self.longitudesRGF93), " ; LenghtPixel = ", len(self.longitudespixels))

  def access(self):
    gpsd.connect()
    packet = gpsd.get_current()
    if packet.mode >= 2:
      latWS84 = packet.lat
      lonWS84 = packet.lon
      bearing = packet.track
      altitude = "NA"
      if packet.mode >=3:
        altitude = packet.alt
    else:
      latWS84 = "NA"
      lonWS84 = "NA"
      bearing = "NA"
      altitude = "NA"

    print("Latitude : ", latWS84, " - Longitude : ", lonWS84)
    print("Bearing : ", bearing, " - Altitude : ", altitude)
    if isinstance(lonWS84, float) & isinstance(latWS84, float):
      lonRGF93, latRGF93 = GpsUtils().conversionWS84toRGF93(lonWS84, latWS84)
      lonP, latP = GpsUtils().interpolation(lonRGF93, latRGF93)
    else:
      lonP = "NA"
      latP = "NA"
    return lonWS84, latWS84, lonP, latP, bearing, altitude

  def deg2rad(self, angle):
    return angle * pi/180

  def conversionWS84toRGF93(self, longitudeWS84, latitudeWS84):
    l0 = self.deg2rad(3)
    lc = self.deg2rad(3)
    phi0 = self.deg2rad(46.5)    # latitude d'origine en radian
    phi1 = self.deg2rad(44)      # 1er parallele automécoïque
    phi2 = self.deg2rad(49)      # 2eme parallele automécoïque

    phi = self.deg2rad(float(latitudeWS84))
    l = self.deg2rad(float(longitudeWS84))

    #calcul des grandes normales
    gN1 = self.a / sqrt(1 - self.e * self.e * sin(phi1) * sin(phi1))
    gN2 = self.a / sqrt(1 - self.e * self.e * sin(phi2) * sin(phi2))

    #calculs des latitudes isométriques
    gl1 = log(tan(pi / 4 + phi1 / 2) * ((1 - self.e * sin(phi1)) / (1 + self.e * sin(phi1))) ** (self.e / 2))
    gl2 = log(tan(pi / 4 + phi2 / 2) * ((1 - self.e * sin(phi2)) / (1 + self.e * sin(phi2))) ** (self.e / 2))
    gl0 = log(tan(pi / 4 + phi0 / 2) * ((1 - self.e * sin(phi0)) / (1 + self.e * sin(phi0))) ** (self.e / 2))
    gl = log(tan(pi / 4 + phi / 2) * ((1 - self.e * sin(phi)) / (1 + self.e * sin(phi))) ** (self.e / 2))

    #calcul de l'exposant de la projection
    n = (log((gN2 * cos(phi2)) / (gN1 * cos(phi1)))) / (gl1 - gl2)

    #calcul de la constante de projection
    c = ((gN1 * cos(phi1)) / n) * exp(n * gl1)
    
    #calcul des coordonnées
    ys = self.y0 + c * exp(-1 * n * gl0)
    unknonwnRGF93_long = self.x0 + c * exp(-1 * n * gl) * sin(n * (l - lc))
    unknonwnRGF93_lat = ys - c * exp(-1 * n * gl) * cos(n * (l - lc))

    return unknonwnRGF93_long.real, unknonwnRGF93_lat.real

  def interpolation(self, longitudeRGF93, latitudeRGF93):
      print("longitudeRGF93 = ", longitudeRGF93, "latitudeRGF93 = ", latitudeRGF93)
      
      indexLong = (np.abs(np.asarray(self.longitudesRGF93)-longitudeRGF93)).argmin()
      indexLat = (np.abs(np.asarray(self.latitudesRGF93)-latitudeRGF93)).argmin()

      longProch = self.longitudesRGF93[indexLong]
      latProch = self.latitudesRGF93[indexLat]

      if longitudeRGF93 <= longProch:
        unknown_longPi = self.longitudespixels[indexLong] - (np.abs(longitudeRGF93 - longProch))/50
      else:
        unknown_longPi = self.longitudespixels[indexLong] + (np.abs(longitudeRGF93 - longProch))/50

      if latitudeRGF93 <= longProch:
        unknown_latPi = self.latitudespixels[indexLat] + (np.abs(latitudeRGF93 - latProch))/self.echelle
      else:
        unknown_latPi = self.latitudespixels[indexLat] - (np.abs(latitudeRGF93 - latProch))/self.echelle

      print("lonPi = ", unknown_longPi, " ; latPi = ", unknown_latPi)
      return unknown_longPi, unknown_latPi