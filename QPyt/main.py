#!/usr/bin/python
import andUI
import androidhelper

droid = androidhelper.Android()

#; pdb.set_trace()
import threading
import os, time, json, math
#import android
from datetime import datetime
import string
import urllib.request, urllib.parse, urllib.error

global startTime
 
def millis():
   """ returns the elapsed milliseconds (1970/1/1) since now """
   dt = datetime.now() - datetime(1970, 1, 1)
   ms = (dt.days * 24 * 60 * 60 + dt.seconds) * 1000 + dt.microseconds / 1000.0
   return str(int(ms))

startTime = millis()
print("startTime= " + startTime)

#droid = android.Android()

class locThread (threading.Thread):
   def __init__(self, threadID, name, oUI, urlServ, delay, duration):
      threading.Thread.__init__(self)
      self.threadID = threadID
      self.name = name
      self.oUI = oUI
      self.counter = 1
      self.delay = delay
      self.lastLoc = {'time': startTime}
      self.dure = duration
      self.url = urlServ
      #self.time = {'time': startTime}
   def run(self):
      print ( self.name + " Starting location...")
      andUI.notify( "Golf Québec", " Starting location...")
      while self.oUI.runflag:   #self.counter:
         res = locate(self.delay)
         if res == {}:
            andUI.toast(str(self.counter) + ' - ' + 'GPS no succes')		 
         if res != {}:
            mess = md = co = ""
            #print(mess)
            dis = 0
            if 'latitude' in self.lastLoc:
               dis = calculDistance(self.lastLoc, res)
            elaps = 0
            elaps = res['time'] - int(self.lastLoc['time']) 
            self.lastLoc = res
            acc = round(res['accuracy'],0)
            md = str(self.counter) + ' - Dist.' + str(dis) + " Alt." + str(res['altitude']) + " Acc." + str(acc)
            co = str(round(res['latitude'],7))  + "\nElaps:" + str(elaps/1000)
            mess = md + "\n" + co
            if self.oUI.runflag:
               andUI.toast(mess)
               andUI.notify(md,co)
               r = set_pos(self.url, res['latitude'], res['longitude'], res['altitude'])
         self.counter += 1
         time.sleep(self.dure)
      print("Exiting " + self.name)


class UIThread():
   def __init__(self, start):
      self.runflag = True
      print ("Starting UIThread...")
      #os._exit(1)

   def run(self,urlServer=None, delay=60):
      if not urlServer:
         ul = readConfig()
         lbl = []
         for s in ul['coll']:
            lbl.append(s['name'])
         #print(str(ul))
         chx = andUI.dialog_list("Select server", lbl)
         for s in ul['coll']:
            if s['name'] == lbl[chx['item']]:
               urlServer = (s['url'])
      
         print( 'urlServer=' + urlServer)  
      thread1 = locThread(1, "Thread-loc", self, urlServer, int(delay), 1)
      thread1.start()
   
   def stop(self):
      self.runflag = False



def locate(DELAI):
  while True:
    droid.startLocating(minDistance=10000)
    time.sleep(DELAI)
    loc = droid.readLocation().result
    if loc == {}:
       print('GPS no succes')
      #return loc
    if loc != {}:
       try:
         n = loc['gps']
       except KeyError:
         n = loc['network']
       #print(str(loc))
       return n
       break
    droid.stopLocating() 

def calculDistance(pt1, pt2):
   lat1 = pt1['latitude']
   lat2 = pt2['latitude']
   lon1 = pt1['longitude']
   lon2 = pt2['longitude']

   R = 6967410.324 # Rayon moyen en verge
   rLat1 = lat1 * (math.pi / 180)
   rLat2 = lat2 * (math.pi / 180)
   dLat = (lat2-lat1) * (math.pi / 180)
   dLon = (lon2-lon1) * (math.pi / 180)
   a = (math.sin(rLat1) * math.sin(rLat2)) + (math.cos(rLat1) * math.cos(rLat2) * math.cos(dLon))
   if abs(a) > 1:
      print('val etror: ' + str(a))
      a = 1
   ac = math.acos(a)

   d = R * ac
   d = round(d)
   #print(str(d))
   return d


def set_pos(urlServ, lat, lng, acc, user = '80'):
  """Post data to golf service"""
  param = "data=%s$%s$%s$%s$%s$%s" % (user, startTime, millis(), str(lat), str(lng), str(acc))
  url = urlServ + 'setPosition?' + param
  resp_json = urllib.request.urlopen(url).read().decode('utf-8')
  return resp_json

def readConfig():
   path = "/storage/emulated/0/qpython/golf/urls.txt"
   f = open(path)
   return json.load(f)

def run(urlServer=None):
   if not urlServer:
      ul = readConfig()
      lbl = []
      for s in ul['coll']:
         lbl.append(s['name'])
      #print(str(ul))
      chx = andUI.dialog_list("Select server", lbl)
      for s in ul['coll']:
         if s['name'] == lbl[chx['item']]:
            urlServer = (s['url'])
      
      print( 'urlServer=' + urlServer)  
   #thread1 = locThread(1, "Thread-loc", urlServer, 60, 5)
   #thread1.start()


def start():
   ui = UIThread(startTime)
   ui.run()

 
#ui = UIThread(startTime)
#start()


# Start new Threads
#thread1.start()

print("Exiting Main Thread")