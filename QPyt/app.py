#!/usr/bin/python
import andUI
import androidhelper

droid = androidhelper.Android()
import pdb
#; pdb.set_trace()
import threading
import os, sys, time, json, math
#import android
from datetime import datetime
import string
import urllib.request, urllib.parse, urllib.error
from multiprocessing import Process

def millis():
   """ returns the elapsed milliseconds (1970/1/1) since now """
   dt = datetime.now() - datetime(1970, 1, 1)
   ms = (dt.days * 24 * 60 * 60 + dt.seconds) * 1000 + dt.microseconds / 1000.0
   return str(int(ms))


class locThread (threading.Thread):
   def __init__(self, threadID, name, oUI, startTime):
      threading.Thread.__init__(self)
      self.threadID = threadID
      self.name = name
      self.oUI = oUI
      self.counter = len(self.oUI.state[1]) + 1
      self.startTime = startTime
      self.lastLoc = {'time': startTime}
      self.isHot = 0
   def run(self):
      self.watch()
   def watch(self, oUI= None, stateRun = 1):
      if oUI:
         self.oUI = oUI
      print ( self.name + " Starting location...")
      andUI.notify( "Golf Québec", " Starting location...")
      self.oUI.state[0]['run'] = stateRun 
      while self.oUI.state[0]['run'] == 1:   #self.counter:
         res = self.locate(self.oUI.state[0]['locDelay'])
         if res == {}:
            andUI.toast(str(self.counter) + ' - ' + 'GPS no succes, locating stopped')		
            self.oUI.state[0]['run'] = 2
            break
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
               if self.oUI.state[0]['optToast'] == 1:
                  andUI.toast(mess)
               if self.oUI.state[0]['optNotify'] == 1:
                  andUI.notify(md,co)
               try:
                  #print('info=' + str(len(self.oUI.state[1])))
                  #if len(self.oUI.state[1]) == 1 or dis >= self.oUI.state[0]['minDist']:
                     print('Dis= ' + str(dis))
                     print('self.isHot= ' + str(self.isHot) )
                     print('self.oUI.state[0]["minDist"]= ' + str(self.oUI.state[0]['minDist']) )					 
                     print('dis <= self.oUI.state[0]["minDist"] and not self.isHot= ' + str(dis <= self.oUI.state[0]['minDist'] and not self.isHot) )					 
                     if dis <= self.oUI.state[0]["minDist"] and not self.isHot:
                        self.isHot = 1;
                        r = self.set_pos(self.oUI.state[0]['url'], res['latitude'], res['longitude'], res['accuracy'], res['time'], self.isHot) 
                        res['sent'] = 0
                        print("Dist : %d rec HOT" % dis)
                     elif dis >= self.oUI.state[0]["minDist"]:
                        self.isHot = 0;
                        r = self.set_pos(self.oUI.state[0]['url'], res['latitude'], res['longitude'], res['accuracy'], res['time'], self.isHot)
                        res['sent'] = 0
                        print("Dist : %d rec" % dis)
                     else:
                        print("Dist : %d NOT rec" % dis)
               except urllib.error.URLError as e:
                  self.oUI.state[2].append(str(e.reason))
                  res['sent'] = 1
                  print(str(self.oUI.state))
            else:   
               self.oUI.state[0]['run'] = 2
               break
         self.counter += 1
         #if self.counter > 2:
            #print(str(res))
            #sys.stderr.close()
            #os._exit(1)
         time.sleep(self.oUI.state[0]['frequence'])
      print("Exiting Watch in " + self.name)
      #os._exit(1)

   def locate(self,DELAI):
     counter = 1
     while True:
       droid.startLocating(minDistance=10000)
       time.sleep(DELAI)
       loc = droid.readLocation().result
       if loc == {}:
          print('GPS no succes')
          nbrErr = len(self.oUI.state[2])
          if nbrErr == 0:
             self.oUI.state[2].append('GPS no succes')
          else:
             self.oUI.state[2][nbrErr-1] = ('GPS no succes %d times' % ( counter))
          counter += 1
      #return loc
       if loc != {}:
          try:
            n = loc['gps']
          except KeyError:
            n = loc['network']
       #print(str(loc))
          return n
          if n['accuracy'] > self.oUI.state[0]['minAcc']:
             break
       droid.stopLocating()
       if self.oUI.state[0]['run'] != 1:
          return {}
          break

   def set_pos(self, urlServ, lat, lng, acc, time, isHot, user = '80'):
     """Post data to golf service"""
     param = "data=%s$%s$%s$%s$%s$%s$%s" % (user, self.startTime, time, str(lat), str(lng), str(acc), str(isHot))
     url = urlServ + 'setPosition?' + param
     #print(url)
     resp_json = urllib.request.urlopen(url).read().decode('utf-8')
     return resp_json
  
  
class UIThread():
   def __init__(self, start):
      self.state = [{"run":1, "userID":'', "curUser":'', "url":'', "locDelay":10, "frequence":1, "minAcc":100, "minDist":20, "optNotify":1, "optToast":1},[], [] ]
      self.locT = None
      self.p = None
      self.startTime = 0
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
      if self.locT == None:
         startTime = millis()
         print("startTime= " + startTime)
         self.startTime = startTime
         self.locT = locThread(1, "Thread-loc", self, startTime)
         self.locT.start()
      else:
         self.locT.watch()
      print(str(self.locT))

   def restart(self):
      if (self.locT):
         while (self.locT.isAlive()):
            time.sleep(1000)
      self.locT = locThread(1, "Thread-loc", self, self.startTime)
      self.locT.start()
      self.state[0]['run'] = 1
      print('RESTARTED with %d location' % len(self.state[1]))
      
 
      
   def stop(self):
      self.state[0]['run'] = 0
      print('isAlive' + str(self.locT.isAlive()))

   def getData():
      return stt(self.state)

def logon( urlServ, user, passw):
   param = "user=%s&passw=%s" % (user, passw)
   url = urlServ + 'identUser?' + param
   print('URL===' + url)
   resp_json = urllib.request.urlopen(url).read().decode('utf-8')
   return resp_json



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




def readConfig():
   path = "/storage/emulated/0/qpython/golf/urls.txt"
   f = open(path)
   return json.load(f)


def start():
   ui = UIThread(startTime)
   ui.run()

 
#ui = UIThread(startTime)
#start()


print("Exiting Main Thread")