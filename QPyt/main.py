debug = True
objUI = oUI = None
curUser = optList = optCheck = ""
optServ = 0
optNotify = optToast = frequence = 1
locDelay = minDist = 20
minAcc = 30
tmpMess = [{},[],[]]
#import app as oUI
#import pdb
#; pdb.set_trace()
from bottle import run, route, debug, template, request, Bottle, ServerAdapter
import json, sys

"""
import androidhelper
droid = androidhelper.Android()
path = "/storage/emulated/0/qpython/golf/"

initConfig = oUI.readConfig()
"""
path = ""
f = open(path + "urls.txt")
initConfig = json.load(f)
#"""

htmlBody = template(path + 'htmlBody.tpl')
output = template(path + 'bottle.tpl')
outputrun = template(path + 'bottlerun.tpl')

def initServList():
   optList = ""
   i = 0
   for s in initConfig['coll']:
      chk = "checked" if i == optServ else ""
      opt = '<label for="opt%s"><input id="opt%s" type="radio" name="server" %s value="%s">%s</input></label><br><br>' % (i, i, chk, i, s['name'])
      optList += opt
      i += 1
   return optList

curUser = initConfig['user']
ioutput = output.replace("$defaultUser", curUser)


def initOutput():
   global oUI, objUI,tmpMess, ioutput, optNotify, optToast, optServ, optList, optCheck, curUser, locDelay, minDist, minAcc, frequence, initConfig
   #pdb.set_trace()
   #optCheck = '<label for="optToast"><input id="optToast" type="checkbox" name="optToast" %s value="toast">Show toast</input></label>' % ("checked" if optToast else "")
   #optCheck += '<label for="optNotify"><input id="optNotify" type="checkbox" name="optNotify" %s value="notify">Show notify</input></label>' % ("checked" if optNotify else "")
   #pdb.set_trace()
   htmlB = htmlBody % (locDelay, frequence, minDist, minAcc, ("checked" if optToast else ""), ("checked" if optNotify else ""))
   ioutput = output.replace("&HTMLbody", htmlB)
   ioutput = ioutput.replace("$defaultUser", curUser)
   ioutput = ioutput.replace("$optionList", initServList())
   if objUI:
      ioutput = ioutput.replace("$action", str(objUI.state))
   else:
      #ioutput = ioutput.replace("$action", str(objUI.state))
      ioutput = ioutput.replace("$action", str(tmpMess))
   return ioutput
   
@route('/start', method='GET')
def start_loc():
    global debug,tmpMess, objUI, oUI, curUser, optNotify, optToast, optServ, optCheck, curUser, locDelay, minDist, minAcc, frequence
    if request.GET.save:
		
        user = request.GET.user.strip()
        passw = request.GET.passw.strip()
        optServ = int(request.GET.server.strip())
        locDelay = int(request.GET.delay.strip())
        frequence = int(request.GET.frequence.strip())
        minDist = int(request.GET.minDist.strip())
        minAcc = int(request.GET.minAcc.strip())
        optToast = request.GET.optToast.strip()
        optNotify = request.GET.optNotify.strip()
        """
        print(str(user))
        print(str(passw))
        print(str(optServ))
        print(str(locDelay))
        print(str(minDist))
        print(str(minAcc))
        print(str(optServ))
        """
        #pdb.set_trace()
        curUser = user
        print(initConfig['coll'][optServ]['url'])
        if oUI:
           if curUser == "" or (True if not objUI else objUI.state[0]['curUser'] != user):
              res = json.loads(oUI.logon(  initConfig['coll'][optServ]['url'] , user, passw))
		   
              if res["resp"]["result"]:
                 userID = res["resp"]["user"]["_id"]
                 #print(str(userID))
              else:
                 #print(str(res["resp"]))
                 tmpMess[2].append("Invalid user or password.")
                 if objUI:
                    objUI.state[2].append("Invalid user or password.")
                 return initOutput()
           
           if not objUI:
              objUI = oUI.UIThread(None)
              objUI.run(True)
              objUI.state[0]['userID'] = str(userID)

           objUI.state[0]['curUser'] = user
           objUI.state[0]['url'] = initConfig['coll'][optServ]['url']
           objUI.state[0]['optToast'] = 1 if optToast else 0
           objUI.state[0]['optNotify'] = 1 if optNotify else 0
           objUI.state[0]['locDelay'] = locDelay
           objUI.state[0]['frequence'] = frequence
           objUI.state[0]['minDist'] = minDist
           objUI.state[0]['minAcc'] = minAcc		   
           
           if objUI.state[0]['run'] != 1:
              print('Main restart run=' + str(objUI.state[0]['run']))
              objUI.restart()
                   
           data = str(objUI.state)
           objUI.state[2] = []
        else:
           print('elseeeeee')
           data = "[{'run':1}, [{'bearing': 0, 'altitude': 118, 'provider': 'gps', 'sent':1, 'dist':122.5, 'longitude': -71.229320759999993, 'time': 1552279052000, 'latitude': 46.803383169999996, 'speed': 0, 'accuracy': 28.822999954223633}, {'bearing': 0, 'altitude': 106, 'provider': 'gps', 'longitude': -71.229327190000006, 'time': 1552279072000, 'latitude': 46.803414740000001, 'speed': 0, 'accuracy': 36.407997131347656}, {'bearing': 0, 'altitude': 105, 'provider': 'gps', 'longitude': -71.229333609999998, 'time': 1552279082000, 'latitude': 46.803432100000002, 'speed': 0, 'accuracy': 43.993000030517578}, {'bearing': 0, 'altitude': 106, 'provider': 'gps', 'longitude': -71.229337099999995, 'time': 1552279093000, 'latitude': 46.80343697, 'speed': 0, 'accuracy': 37.924999237060547}, {'bearing': 0, 'altitude': 104, 'provider': 'gps', 'longitude': -71.229331790000003, 'time': 1552279104000, 'latitude': 46.803439650000001, 'speed': 0, 'accuracy': 42.475997924804688}, {'bearing': 0, 'altitude': 104, 'provider': 'gps', 'longitude': -71.229335419999998, 'time': 1552279113000, 'latitude': 46.803443989999998, 'speed': 0, 'accuracy': 31.856998443603516}, {'bearing': 0, 'altitude': 105, 'provider': 'gps', 'longitude': -71.229342919999993, 'time': 1552279124000, 'latitude': 46.803447179999999, 'speed': 0, 'accuracy': 56.128997802734375}], ['Erreur1']]"
        if objUI and debug:
           print('main start state=' + str(objUI.state[0]['run']))
        return outputrun.replace("$action", data)
		#'<p>The new task was inserted into the database, the ID is %s</p>' 
        #% new_id
    if request.GET.cancel:
        print("EXIT")
        sys.stderr.close()
        #pdb.set_trace()

@route('/stop', method='GET')
def stop_ref():
   global debug, objUI, oUI, optNotify, optToast, optServ, optCheck
   if request.GET.stop:
      #pdb.set_trace()
      if oUI:
         objUI.stop()
         return outputrun.replace("$action", str(objUI.state))
      else:	#Local
         return initOutput()

   if request.GET.view:
      if oUI:
         if debug:
            print('main view state=' + str(objUI.state[0]['run']))
         droid.webViewShow('https://cdore.ddns.net/localMap.html')
      return outputrun.replace("$action", str(objUI.state))

   if request.GET.refresh:
      if oUI and debug:
         print('main refresh state=' + str(objUI.state[0]['run']))
      return outputrun.replace("$action", str(objUI.state))
      
   if request.GET.start:
      if oUI and debug:
         objUI.state[2] = []
         print('main refresh start state=' + str(objUI.state[0]['run']))
      return initOutput()
         
   else:
     return output

@route('/', method='GET')
def default():
   return initOutput()
 
	#add this at the very end:
	#debug(True)
	#run(reloader=True)
if oUI:
   droid.webViewShow('http://localhost:8080/')
run(quiet=True)
#run()