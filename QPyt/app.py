#!/usr/bin/python
import andUI
import androidhelper

droid = androidhelper.Android()

#; pdb.set_trace()
import threading
import os, sys, time, json, math
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
      #oUi.locT = self
      self.counter = 1
      self.delay = delay
      self.lastLoc = {'time': startTime}
      self.dure = duration
      self.url = urlServ
      #oUi.locT = self.lastLoc
      #self.time = {'time': startTime}
   def run(self):
      print ( self.name + " Starting location...")
      andUI.notify( "Golf Québec", " Starting location...")
      while self.oUI.state[0]['run'] == 1:   #self.counter:
         res = locate(self.delay)
         if res == {}:
            andUI.toast(str(self.counter) + ' - ' + 'GPS no succes')		 
         if res != {}:
            mess = md = co = ""
            #print(mess)
            self.oUI.state[1].append( res)
            dis = 0
            if 'latitude' in self.lastLoc:
               dis = calculDistance(self.lastLoc, res)
               res['dist'] = dis
            elaps = 0
            elaps = res['time'] - int(self.lastLoc['time']) 
            self.lastLoc = res
            acc = round(res['accuracy'],0)
            md = str(self.counter) + ' - Dist.' + str(dis) + " Alt." + str(res['altitude']) + " Acc." + str(acc)
            co = str(round(res['latitude'],7))  + "\nElaps:" + str(elaps/1000)
            mess = md + "\n" + co
            if self.oUI.state[0]['run'] == 1:
               andUI.toast(mess)
               andUI.notify(md,co)
               try:
                  r = set_pos(self.url, res['latitude'], res['longitude'], res['altitude'])
                  res['sent'] = 0
               except:
                  self.oUI.state[2] = urllib.error.URLError
                  res['sent'] = 1
            else:   
               self.oUI.state[0]['run'] = 2
         self.counter += 1
         #if self.counter > 2:
            #print(str(res))
            #sys.stderr.close()
            #os._exit(1)
         time.sleep(self.dure)
      print("Exiting " + self.name)
      #os._exit(1)


class UIThread():
   def __init__(self, start):
      self.state = [{"run":1, "curUser":"", "optNotify":1, "optToast":1},[], [] ]
      self.locT = None
      print ("Starting UIThread...")
      #os._exit(1)

   def run(self,urlServer=None, delay=5):
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
      self.state[0]['run'] = 0

   def getData():
      return stt(self.state)

def logon( urlServ, user, passw):
   param = "user=%s&pass=%s" % (user, passw)
   url = urlServ + 'identUser?' + param
   print(url)
   resp_json = urllib.request.urlopen(url).read().decode('utf-8')
   return resp_json

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


print("Exiting Main Thread")