  # MongoDB
import pymongo
from pymongo import MongoClient
import phonetics

dbase = "golf"
port = 27017
uri = "mongodb://localhost"

DBclient = MongoClient(uri, port)
data = DBclient[dbase]

col = data.club

docs = col.find({}, {"_id": 1,"nom": 1})
#docs = col.find({"_id": 3})

print(str(docs.count()))

def scanName(name):
	for car in name:
		if (wa.find(car)) > 0:
			pos = wa.find(car)
			name = name.replace(car, na[pos:pos+1], 1)
	return name.upper()

for rec in docs:
	wa = "àâäôóéèëêïîçùûüÿÀÂÄÔÉÈËÊÏÎŸÇÙÛÜ"
	na = "aaaooeeeeiicuuuyAAAOEEEEIIYCUUU"
	print(str(rec))
	r=phonetics.dmetaphone(rec["nom"])
	res = scanName(str(rec["nom"]))
	print(r[0] + "  -  " + res)
	pRep = col.update({"_id":rec["_id"]}, {"$set":{"nomP": r[0], "nomU": res }})
	#print(str(rec["nom"]))
	
"""
for rec in docs
	print(str(rec))
	
r=phonetics.dmetaphone('Metropolitain')
r[0]
"""