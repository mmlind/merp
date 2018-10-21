# coding: utf-8

from pymongo import MongoClient
from bson.objectid import ObjectId

from data_model import *

from bson import json_util
import json


client = MongoClient('localhost:27017')

db = client.merp	# specfy the name of the database e.g. "merp"




def get_records(cls):
	"""
	Returns all objects of a given class 
	The target collection is derived from the object's class 
	and referenced via a CLASS->COLLECTION mapping table [DB_COLLECTIONS] 
	"""

	cls_name = cls.__name__

	col_name = DB_COLLECTIONS[cls_name]		# name of the database collection

	objs = []

	try:

		cursor = db[col_name].find()

		for c in cursor:

			c['_id'] = str(c['_id']) 		# replace ObjectId-syntax with string

			obj = cls(c)

			objs.append(obj)

	except Exception, e:

		print("DB ERROR: collection [%s] command [%s] error: %s" % (col_name, 'find', str(e)))

	return objs




def insert_record(obj):
	"""
	Inserts an object into the database.
	The target collection is derived from the object's class 
	and referenced via a CLASS->COLLECTION mapping table [DB_COLLECTIONS] 
	"""

	cls_name = type(obj).__name__
	col_name = DB_COLLECTIONS[cls_name]						# name of the database collection

	success = False

	try:
		obj.__dict__.pop('_id', None)						# remove the object ID to force creating a random new one

		jd = json.dumps(obj, default=lambda o: o.__dict__)	# convert into a json document 
		mo = json.loads(jd)									# convert into a dictionary

		result = db[col_name].insert_one(mo)

		success = result.inserted_id

	except Exception, e:

		print("DB ERROR: collection [%s] command [%s] error: %s" % (col_name, 'insert_one', str(e)))

	return success




def update_record(obj):
	"""
	Updates an object in the database.
	The object is referenced using Mongo's default _ID field.
	The target collection is derived from the object's class 
	and referenced via a CLASS->COLLECTION mapping table [DB_COLLECTIONS] 
	"""

	cls_name = type(obj).__name__
	col_name = DB_COLLECTIONS[cls_name]						# name of the database collection

	success = False

	try:

		sid = obj._id

		obj.__dict__.pop('_id', None)						# remove the object ID from the update set
		jd = json.dumps(obj, default=lambda o: o.__dict__)	# convert into a json document 
		mo = json.loads(jd)									# convert back into mongo-accepted object

		cursor = db[col_name].update_one({"_id":ObjectId(sid)}, {"$set": mo}, upsert=True)

		# cursor = db.purchaseorders.update_one({"_id":ObjectId(obj._id)},{"$set":{"datetime":obj.datetime,"status":obj.status, "supplier":obj.supplier, "items":obj.items, "total":obj.total}}, upsert=True)
		success = (cursor.matched_count == 1)
    
	except Exception, e:

		print("DB ERROR: collection [%s] command [%s] error: %s" % (col_name, 'update_one', str(e)))

	return success




def get_record(cls, oid):
	"""
	Loads an object from the database by specifying CLASS and _ID
	The target collection is derived from the object's class 
	and referenced via a CLASS->COLLECTION mapping table [DB_COLLECTIONS] 
	"""

	col_name = DB_COLLECTIONS[cls.__name__]						# name of the database collection

	obj = cls()

	if (oid=='0' or oid==''):
		return obj

	try:

		c = db[col_name].find_one({"_id": ObjectId(oid)})
		c['_id'] = oid 		# replace ObjectId-syntax with string

		obj = cls(c)
		# obj =PurchaseOrder(c[u'_id'], c[u'datetime'], c[u'status'], c[u'supplier'], c[u'items'], c[u'total'])

	except Exception, e:

		print("DB ERROR: collection [%s] command [%s] error: %s" % (col_name, 'find_one', str(e)))

	return obj




def delete_record(cls, oid):
	"""
	Removes an existing object, specified by CLASS and _ID, from the database. 
	The target collection is derived from the object's class 
	and referenced via a CLASS->COLLECTION mapping table [DB_COLLECTIONS] 
	"""

	col_name = DB_COLLECTIONS[cls.__name__]						# name of the database collection
	success = False

	try:
		cursor = db[col_name].delete_one({"_id":ObjectId(oid)})
		success = (cursor.deleted_count == 1)
    
	except Exception, e:

		print("DB ERROR: collection [%s] command [%s] error: %s" % (col_name, 'delete_one', str(e)))

	return success




def get_units():
	"""
	List of all material units available -- in ENGLISH.
	The English word is used as the key for language translation.
	"""

	return ['piece','kg','liter','box','barrel','bag','can','block','set','sheet','cup','bar','slice','bottle','case','yard','meter','tin','sack','roll','one']



