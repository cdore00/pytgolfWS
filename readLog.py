
import os, time
import datetime

import pymongo
from pymongo import MongoClient
dbase = "golf"
port = 27017
uri = "mongodb://localhost"
DBclient = MongoClient(uri, port)
data = DBclient[dbase]

NGINX_LOG_DIR = ""
fileName = "golf.access.log"

#os.remove("ChangedFile.csv") 
#os.rename(src, dst)

def run():

	try:
		#os.remove(NGINX_LOG_DIR + fileName + ".dat")
		x=1
	except:
		pass
	
	"""
	endTime = time.time()+5
	while True:
		if endTime < time.time():
			print("Can't rename")
			break
		else:
			try:
				os.rename(fileName, fileName + ".dat")
				loadFile()
				break
			except:
				pass
	"""
	loadFile()

def loadFile():

	lines = [line.rstrip('\n') for line in open(NGINX_LOG_DIR + fileName + ".dat")]
	cnt = 1
	arrList = []
	for line in lines:
		
		try:
			fields = [x.strip() for x in line.split("|")]
			date, status, ip, request, user_agent, referer = fields
			print(request)
			if len(referer) > 5:
				status_code = int(status)
				sd = date
				para = [x for x in date.split(" ")]
				sd = para[0]
				dif = int(para[1])/100
				dt = datetime.datetime.strptime(sd, "%d/%b/%Y:%H:%M:%S")
				dt = time.mktime(dt.timetuple())*1000
				#print(date + str(dt))
				elLog = { "time": dt, "date": date, "status": status_code, "ip": ip, "request": request, "referer": referer, "user_agent": user_agent}
				arrList.append(elLog)
				cnt += 1
		except (ValueError, IndexError) as e:
			# Not good, print it!
			print("WARNING: parsing log failed", e)
			print(line)
			continue
		#if not harmless(status_code, ip, request, user_agent):
			#print(line)
		
		if cnt > 50:
			insertLogList(arrList)
			arrList = []
			cnt = 1
	if cnt > 1:
		insertLogList(arrList)
	#print(str(cnt))

def harmless(status_code, ip, request, user_agent):
     # ... some checks using ip and user agent ...

    if status_code >= 200 and status_code < 400:
        return True

    # used by nginx
    if status_code == 499:
        return True

    # We've filtered all the goodness:
    return False

def insertLogList(listLog):
	""" To insert log items list"""
	try:
		if listLog:
			#print(str(listLog))
			coll = data.log
			doc = coll.insert(listLog)
			print(str(doc))
		else:	
			return("No param")		
	except Exception as ex:
		#return except_handler("confInsc", ex)
		print("error " + str(doc))
		x=1
		
	
run()
