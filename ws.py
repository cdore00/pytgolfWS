import random
import string
import cherrypy

import pdb
#; pdb.set_trace()
import sys, os, io, time, re, cgi, csv, urllib.parse
from urllib.parse import urlparse, parse_qs
from sys import argv
from datetime import datetime


HOSTserv = 'http://127.0.0.1:3000/'
HOSTclient = 'http://localhost:8080/'
HOSTcors = 'https://cdore00.github.io'
#self.headers["Host"] == 'cdore.ddns.net'

global logPass 
logPass = ""
if os.getenv('PINFO') is not None:
	logPass = os.environ['PINFO']

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

client = MongoClient(uri, port)
data = client[dbase]
from bson import ObjectId
from bson.json_util import dumps
from bson.json_util import loads
import json

import golfFunc as gf
gf.data = data

def exception_handler(status, message, traceback, version):
	#pdb.set_trace()
	logInfo = "ERROR " + status + " : " + message + " : Command: " +  cherrypy.request.path_info + "?" + cherrypy.request.query_string
	print(traceback)
	print(logInfo)
	gf.log_Info(logInfo)
	return logInfo


class webServer(object):

    @cherrypy.expose
    def index(self, info = False):
        randId = ''.join(random.sample(string.hexdigits, 8))
        return 'Call ID: ' + randId

    @cherrypy.expose
    def getRegions(self, info = False):
        #pdb.set_trace()
        cookies = cherrypy.request.cookie        
        cookie = cherrypy.response.cookie
        cookie['tcookie'] = 'testcookieValue'
        cookie['tcookie']['max-age'] = 3600

        query_components = parse_qs(urlparse('url?' + info).query)
        col = data.regions
        docs = col.find({})
        res = dumps(docs)
        return res
		
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
    def getBloc(self, info = False):
        param = parse_qs(urlparse('url?' + info).query)
        return gf.getBloc(param, self)

    @cherrypy.expose
    def getClubParcTrous(self, info = False):
        param = parse_qs(urlparse('url?' + info).query)
        return gf.getClubParcTrous(param, self)

    @cherrypy.expose
    def identUser(self, info = False):
        cookie = cherrypy.response.cookie
        param = parse_qs(urlparse('url?' + info).query)
        return gf.authUser(param, self, cookie)

    @cherrypy.expose
    #@cherrypy.tools.json_in()
    def listLog(self, passw = ""):
        #pdb.set_trace()
        """ param = info
        if (param != False):
            param = parse_qs(urlparse('url?' + info).query)""" 
        return gf.listLog(passw, logPass)
		
    @cherrypy.expose
    def showLog(self, nam = ''):
        return gf.showLog(nam)		
		
		
		
		
# Start server listening request
def run( port = 8080, domain = '0.0.0.0'):
   origin = '*'
   config = {'server.socket_host': domain,
             'server.socket_port': port,   
             'tools.response_headers.on': True, 
			 'tools.response_headers.headers': [ ('Access-Control-Allow-Origin', origin)],
			 'error_page.default': exception_handler}
   cherrypy.config.update(config)
   gf.log_Info('Sarting Web server...(' + domain + ":" + str(port) + ')') 
   print('Sarting Web server...(' + domain + ":" + str(port) + ')')   
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