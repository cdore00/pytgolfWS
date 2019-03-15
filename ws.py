import random
import string
import cherrypy

import pdb
#; pdb.set_trace()
import sys, os, io, time, re, cgi, csv, urllib.parse
from urllib.parse import urlparse, parse_qs
from sys import argv
from datetime import datetime
# JSON
from bson import ObjectId
from bson.json_util import dumps
from bson.json_util import loads
import json

LOCAL_HOST = 'http://127.0.0.1:3000/'
HOSTserv = LOCAL_HOST
HOSTclient = 'http://localhost:8080/'
HOSTcors = '*'
#'https://cdore00.github.io'

global logPass 
logPass = ""
if os.getenv('PINFO') is not None:
	logPass = os.environ['PINFO']
	
if os.getenv('HOST') is not None:
	HOSTcors = os.environ['HOST']
	
# MongoDB
import pymongo
from pymongo import MongoClient

dbase = "golf"
port = 27017
uri = "mongodb://localhost"
if os.environ.get('MONGODB_USER'):
	port = int(os.environ['MONGODB_PORT'])
	user = urllib.parse.quote_plus(os.environ['MONGODB_USER'])
	passw = urllib.parse.quote_plus(os.environ['MONGODB_PASSWORD'])
	domain = urllib.parse.quote_plus(os.environ['MONGODB_SERVICE'])
	dbase = urllib.parse.quote_plus(os.environ['MONGODB_DATABASE'])
	uri = "mongodb://%s:%s@%s/%s?authMechanism=SCRAM-SHA-1" % (user, passw, domain, dbase)
	if domain == "192.168.10.11":
		HOSTclient = 'https://cdore.ddns.net/'
		HOSTserv = 'https://cdore.ddns.net/pyt/'
	else:
		HOSTclient = 'https://cdore00.github.io/golf/'
		HOSTserv = 'https://pytgolf-cd-serv.1d35.starter-us-east-1.openshiftapps.com/'
		#HOSTclient = 'https://pytgolf-cdore2.a3c1.starter-us-west-1.openshiftapps.com/'
	print("HOSTclient=" + HOSTclient)

DBclient = MongoClient(uri, port)
data = DBclient[dbase]
# END MongoDB

""" Golf functions """
import golfFunc as gf
gf.dataBase = data


def exception_handler(status, message, traceback, version):
	""" EXCEPTION """
	#pdb.set_trace()
	logInfo = "ERROR " + status + " : " + message + " : Command: " +  cherrypy.request.path_info + "?" + cherrypy.request.query_string
	print(traceback)
	print(logInfo)
	gf.log_Info(logInfo)
	return logInfo



class webServer(object):
    """ Serve Golf functions """
    def __init__(self):
        gf.logPass = logPass
        #print('logPass=' + logPass)
		
    @cherrypy.expose
    def index(self, info = False):
        randId = ''.join(random.sample(string.hexdigits, 8))
        return 'Call ID: ' + randId

    @cherrypy.expose
    def getRegions(self, info = False):
        #pdb.set_trace()
        """ cookies = cherrypy.request.cookie        
        cookie = cherrypy.response.cookie
        cookie['tcookie'] = 'testcookieValue'
        cookie['tcookie']['max-age'] = 3600 """

        col = gf.dataBase.regions
        docs = col.find({})
        res = dumps(docs)
        return res

    @cherrypy.expose
    def getFav(self, info = False):
        param = parse_qs(urlparse('url?' + info).query)
        return gf.getFav(param, self)

    @cherrypy.expose
    def updateFav(self, info = False):
        param = parse_qs(urlparse('url?' + info).query)
        return gf.updateFav(param, self)
		
    @cherrypy.expose
    def searchResult(self, info = False):
        param = parse_qs(urlparse('url?' + info).query)
        return gf.searchResult(param, self)

    @cherrypy.expose
    def getClubList(self, info = False):
        param = parse_qs(urlparse('url?' + info).query)
        return gf.getClubList(param, self)

    @cherrypy.expose
    def getClubData(self, info = False):
        param = parse_qs(urlparse('url?' + info).query)
        return gf.getClubData(param, self)

    @cherrypy.expose
    def getClubParc(self, info = False):
        param = parse_qs(urlparse('url?' + info).query)
        return gf.getClubParc(param, self)

    @cherrypy.expose
    def getParcInfo(self, info = False):
        param = parse_qs(urlparse('url?' + info).query)
        return gf.getParcInfo(param, self)
		
    @cherrypy.expose
    def setGolfGPS(self, info = False):
        gf.cookie = cherrypy.request.cookie
        param = parse_qs(urlparse('url?' + info).query)
        return gf.setGolfGPS(param, self)

    @cherrypy.expose
    def saveClub(self, info = False):
        gf.cookie = cherrypy.request.cookie
        param = parse_qs(urlparse('url?' + info).query)
        return gf.saveClub(param, self)
		
    @cherrypy.expose
    def getClubParcTrous(self, info = False):
        param = parse_qs(urlparse('url?' + info).query)
        return gf.getClubParcTrous(param, self)
		
    @cherrypy.expose
    def getBloc(self, info = False):
        param = parse_qs(urlparse('url?' + info).query)
        return gf.getBloc(param, self)

    @cherrypy.expose
    def identUser(self, info = False, user = False, passw = False):
        if user:
           info = "user=" + user + "&pass=" + passw
        cookieOut = cherrypy.response.cookie
        param = parse_qs(urlparse('url?' + info).query)
        return gf.authUser(param, self, cookieOut)

    @cherrypy.expose
    #@cherrypy.tools.json_in()
    def listLog(self, passw = ""): 
        return gf.listLog(passw, logPass)
		
    @cherrypy.expose
    def showLog(self, name = ''):
        #pdb.set_trace()
        if "?" in name:
            param = parse_qs(urlparse(name).query)
            param = param['name'][0]
        else:
            param = name
        return gf.showLog(param)		

    @cherrypy.expose
    def getUser(self, info = False):
        gf.cookie = cherrypy.request.cookie
        param = parse_qs(urlparse('url?' + info).query)
        return gf.getUserInfo(param, self)

    @cherrypy.expose
    def saveUser(self, info = False):
        param = parse_qs(urlparse('url?' + info).query)
        return gf.saveUser(param, self)

    @cherrypy.expose
    def getPassForm(self):
        return gf.getPassForm(self)

    @cherrypy.expose
    def savePass(self, info = False):
        gf.cookie = cherrypy.request.cookie
        param = parse_qs(urlparse('url?' + info).query)
        return gf.savePassword(param, self)
		
    @cherrypy.expose
    def addUserIdent(self, info = False):
        param = parse_qs(urlparse('url?' + info).query)
        return gf.addUserIdent(param, HOSTclient, HOSTserv, self)

    @cherrypy.expose
    def updUser(self, info = False):
        param = parse_qs(urlparse('url?' + info).query)
        return gf.updateUser(param, self)
		
    @cherrypy.expose
    def confInsc(self, data = False):
        pos = cherrypy.request.query_string.find('?')
        info = cherrypy.request.query_string[pos+1:]
        param = parse_qs(urlparse('url?' + info).query)
        return gf.confInsc(param, HOSTclient, self)

    @cherrypy.expose
    def getPass(self, info = False):
        param = parse_qs(urlparse('url?' + info).query)
        return gf.getPass(param, self)		
	
    @cherrypy.expose
    def updateUser(self, info = False):
        gf.cookie = cherrypy.request.cookie
        param = parse_qs(urlparse('url?' + info).query)
        return gf.updateUser(param, self)
	
    @cherrypy.expose
    def savePassword(self, info = False):
        gf.cookie = cherrypy.request.cookie
        param = parse_qs(urlparse('url?' + info).query)
        return gf.savePassword(param, self)		

    @cherrypy.expose
    def endDelGame(self, info = False):
        gf.cookie = cherrypy.request.cookie
        param = parse_qs(urlparse('url?' + info).query)
        return gf.endDelGame(param, self)	

    @cherrypy.expose
    def getGolfGPS(self, info = False):
        param = parse_qs(urlparse('url?' + info).query)
        return gf.getGolfGPS(param, self)

    @cherrypy.expose
    def getGame(self, info = False):
        param = parse_qs(urlparse('url?' + info).query)
        return gf.getGame(param, self)		

    @cherrypy.expose
    def countUserGame(self, info = False):
        param = parse_qs(urlparse('url?' + info).query)
        return gf.countUserGame(param, self)

    @cherrypy.expose
    def getGameList(self, info = False, user = False, parc = False, skip = False, limit = False, is18 = False, date = False, tele = False, rand = False):
        #pdb.set_trace() 
        if user and isinstance(parc, (list)):
            pos = cherrypy.request.query_string.find('?')
            info = cherrypy.request.query_string[pos+1:]
        elif user:
            info = "user=" + user + "&parc=" + parc + "&skip=" + skip + "&limit=" + limit + "&is18=" + is18  + "&date=" + date + "&tele=" + tele
        param = parse_qs(urlparse('url?' + info).query)
        return gf.getGameList(param, cherrypy)
		
    @cherrypy.expose
    def updateGame(self, info = False):
        param = parse_qs(urlparse('url?' + info).query)
        return gf.updateGame(param, self)
		
    @cherrypy.expose
    def getGameTab(self, info = False):
        param = parse_qs(urlparse('url?' + info).query)
        return gf.getGameTab(param, self)

    @cherrypy.expose
    def endDelGame(self, info = False):
        gf.cookie = cherrypy.request.cookie
        param = parse_qs(urlparse('url?' + info).query)
        return gf.endDelGame(param, self)
		
    @cherrypy.expose
    def delClub(self, info = False):
        param = parse_qs(urlparse('url?' + info).query)
        return gf.delClub(param, self)

    @cherrypy.expose
    def setPosition(self, info = False, data= False):
        if (data):
           info = "data=" + data
        param = parse_qs(urlparse('url?' + info).query)
        return gf.setPosition(param, self)

    @cherrypy.expose
    def getPosition(self, info = False):
        param = parse_qs(urlparse('url?' + info).query)
        return gf.getPosition(param, self)


# Start server listening request
def run( port = 8080, domain = '0.0.0.0'):
   origin = HOSTcors
   print('HOSTcors=' + HOSTcors)
   config = {'server.socket_host': domain,
             'server.socket_port': port,   
             'tools.response_headers.on': True, 
			 'tools.response_headers.headers': [ ('Access-Control-Allow-Origin', origin)],
			 'error_page.default': exception_handler,
			 'engine.autoreload.on' : False,
			 'log.screen': True,
			 'log.access_file': '',
             'log.error_file': ''}
   cherrypy.config.update(config)
   gf.log_Info('Starting Web server...(' + HOSTserv + ":" + str(port) + ')') 
   print('Starting Web server...(' + HOSTserv + ":" + str(port) + ')')   
   if HOSTserv == LOCAL_HOST:
        gf.localHost = True
   cherrypy.quickstart(webServer())	

        
def build_arg_dict(arg):
	argd = dict()
	def add_dict(item):
		i = 0
		for x in arg:
			if x == item:
			  argd[x] = arg[i+1]
			else:
			  i+= 1

	if "port" in arg:
		add_dict("port")
	if "domain" in arg:
		add_dict("domain")
	if "pass" in arg:
		add_dict("pass")
	if "cors" in arg:
		add_dict("cors")
		
	if (len(arg) / 2) != len(argd):
		return False
	else:
		return argd

if __name__ == "__main__":
	#print(argv[0])
	#pdb.set_trace()
	if len(argv) > 1:
		arg = [x for x in argv]
		del arg[0]
		param = build_arg_dict(arg)
		if param:
			if "cors" in param:
				HOSTcors = param["cors"]
				print("CORS= " + HOSTcors)
			#print(str(len(argv)))
			if "pass" in param:
				#global logPass 
				logPass = param["pass"]
				if len(argv) == 3:
					run()
				if "domain" in param and "port" in param:
					run(domain=(param["domain"]), port=int(param["port"]))
				elif "domain" in param:
					run(domain=(param["domain"]))
				elif "port" in param:
					run(port=int(param["port"]))
			else:
				run()
		else:
			print("[domain VALUE] [port VALUE] [pass VALUE]")
	else:
		run()