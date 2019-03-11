import main as oUI
import pdb
#; pdb.set_trace()
from bottle import run, route, debug, template, request, Bottle, ServerAdapter
import json, sys

objUI = False

import androidhelper
droid = androidhelper.Android()
output = template('/storage/emulated/0/qpython/golf/bottle.tpl')

ul = oUI.readConfig()
path = "/storage/emulated/0/qpython/golf/"

"""
path = ""
f = open(path + "urls.txt")
ul = json.load(f)
"""
output = template(path + 'bottle.tpl')
outputrun = template(path + 'bottlerun.tpl')
optList = ""
i = 1
for s in ul['coll']:
   chk = "checked" if i == 1 else ""
   opt = '<label for="opt%s"><input id="opt%s" type="radio" name="server" %s value="%s">%s</input></label><br><br>' % (i, i, chk, s['url'], s['name'])
   print(opt)
   optList += opt
   i += 1

output = output.replace("$defaultUser", ul['user'])
output = output.replace("$optionList", optList)
#outputrun = outputrun.replace("$action", "Starting location...")

@route('/start', method='GET')
def start_loc():

    if request.GET.save:
		
        user = request.GET.user.strip()
        passw = request.GET.passw.strip()
        serv = request.GET.server.strip()
        delay = request.GET.delay.strip()
        print(str(user))
        print(str(passw))
        print(str(serv))
        print(str(delay))
        
        if oUI:
           #pdb.set_trace()
           global objUI
           objUI = oUI.UIThread(None)
           objUI.run(serv, delay= delay)
        #return outputrun.replace("$action", "Starting location...")
        return outputrun.replace("$action", str(objUI.runflag))
		#'<p>The new task was inserted into the database, the ID is %s</p>' 
        #% new_id
    if request.GET.cancel:
        print("EXIT")
        sys.stderr.close()
        #pdb.set_trace()

@route('/stop', method='GET')
def stop_ref():
   if request.GET.stop:
      #pdb.set_trace()
      global objUI
      objUI.stop()
	  if objUI.runflag[0] == 2:
         return output
      else:
         return outputrun.replace("$action", str(objUI.runflag))
	  
   if request.GET.refresh:
      global objUI
      #dat = objUI.getData()
      #print(str(dat)) 
      return outputrun.replace("$action", str(objUI.runflag))

   else:
     return output

@route('/', method='GET')
def default():
   return output
 
	#add this at the very end:
	#debug(True)
	#run(reloader=True)
if oUI:
   droid.webViewShow('http://localhost:8080/')
run()
