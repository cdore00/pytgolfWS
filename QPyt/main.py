objUI = oUI = None
curUser = optNotify = optToast = optServ = optList = optCheck = ""

#import app as oUI
import pdb
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
output = template(path + 'bottle.tpl')
outputrun = template(path + 'bottlerun.tpl')

i = 1
for s in initConfig['coll']:
   chk = "checked" if i == 1 else ""
   opt = '<label for="opt%s"><input id="opt%s" type="radio" name="server" %s value="%s">%s</input></label><br><br>' % (i, i, chk, s['url'], s['name'])
   #print(opt)
   optList += opt
   i += 1

curUser = initConfig['user']
ioutput = output.replace("$defaultUser", curUser)


def initOutput():
   global ioutput, optNotify, optToast, optServ, optList, optCheck, curUser
   
   optCheck = '<label for="optToast"><input id="optToast" type="checkbox" name="optToast" %s value="toast">Show toast</input></label>' % ("checked" if optToast else "")
   optCheck += '<label for="optNotify"><input id="optNotify" type="checkbox" name="optNotify" %s value="notify">Show notify</input></label>' % ("checked" if optNotify else "")
   #pdb.set_trace()
   ioutput = output.replace("$defaultUser", curUser)
   ioutput = ioutput.replace("$optionList", optList)
   ioutput = ioutput.replace("$optCheck", optCheck)
   return ioutput

@route('/start', method='GET')
def start_loc():
    global objUI, oUI, optNotify, optToast, optServ, optList, optCheck, curUser
    if request.GET.save:
        
        user = request.GET.user.strip()
        passw = request.GET.passw.strip()
        optServ = request.GET.server.strip()
        delay = request.GET.delay.strip()
        optToast = request.GET.optToast.strip()
        optNotify = request.GET.optNotify.strip()
		
        print(str(user))
        
        curUser = user

        if oUI:
           #pdb.set_trace()
           objUI = oUI.UIThread(None)
           objUI.run(optServ, delay= delay)
           data = str(objUI.state)
        else:
           data = "[{'run':1}, [{'bearing': 0, 'altitude': 118, 'provider': 'gps', 'sent':1, 'dist':122.5, 'longitude': -71.229320759999993, 'time': 1552279052000, 'latitude': 46.803383169999996, 'speed': 0, 'accuracy': 28.822999954223633}, {'bearing': 0, 'altitude': 106, 'provider': 'gps', 'longitude': -71.229327190000006, 'time': 1552279072000, 'latitude': 46.803414740000001, 'speed': 0, 'accuracy': 36.407997131347656}, {'bearing': 0, 'altitude': 105, 'provider': 'gps', 'longitude': -71.229333609999998, 'time': 1552279082000, 'latitude': 46.803432100000002, 'speed': 0, 'accuracy': 43.993000030517578}, {'bearing': 0, 'altitude': 106, 'provider': 'gps', 'longitude': -71.229337099999995, 'time': 1552279093000, 'latitude': 46.80343697, 'speed': 0, 'accuracy': 37.924999237060547}, {'bearing': 0, 'altitude': 104, 'provider': 'gps', 'longitude': -71.229331790000003, 'time': 1552279104000, 'latitude': 46.803439650000001, 'speed': 0, 'accuracy': 42.475997924804688}, {'bearing': 0, 'altitude': 104, 'provider': 'gps', 'longitude': -71.229335419999998, 'time': 1552279113000, 'latitude': 46.803443989999998, 'speed': 0, 'accuracy': 31.856998443603516}, {'bearing': 0, 'altitude': 105, 'provider': 'gps', 'longitude': -71.229342919999993, 'time': 1552279124000, 'latitude': 46.803447179999999, 'speed': 0, 'accuracy': 56.128997802734375}], ['Erreur1']]"
        return outputrun.replace("$action", data)

    if request.GET.cancel:
        print("EXIT")
        sys.stderr.close()


@route('/stop', method='GET')
def stop_ref():
   global objUI, oUI, optNotify, optToast, optServ, optList, optCheck
   if request.GET.stop:
      #pdb.set_trace()
      if oUI:
         objUI.stop()
         return outputrun.replace("$action", str(objUI.state))
      else:	#Local
         #pdb.set_trace()
         return initOutput()
	  
   if request.GET.refresh:
      return outputrun.replace("$action", str(objUI.state))
	  
   if request.GET.start:
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
run()
