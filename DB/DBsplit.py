import discord
from tinydb import TinyDB, Query
from tinydb.operations import delete
import datetime as dt
import time as t
import json
from core import welcome as wel
from gems import gemsFonctions as GF
from DB import DB


def splitDB(source, destination):
	#DB1 = source
	#DB2 = destination
	t = DB.taille(source)
	print(t)
	i = 1
	while i < t:
		ID = DB.userID(i, source)
		print(ID)
		if destination == "DB/bastionDB":
			DB.newPlayer(ID, destination, "DB/fieldTemplate")
			DB.updateField(ID, "ID", ID, destination)
			DB.updateField(ID, "arrival", DB.valueAt(ID, "arrival", source), destination)
			DB.updateField(ID, "nbMsg", DB.valueAt(ID, "nbMsg", source), destination)
			DB.updateField(ID, "lvl", DB.valueAt(ID, "lvl", source), destination)
			DB.updateField(ID, "xp", DB.valueAt(ID, "xp", source), destination)
			DB.updateField(ID, "parrain", DB.valueAt(ID, "parrain", source), destination)
			DB.updateField(ID, "filleul", DB.valueAt(ID, "filleul", source), destination)

		elif destination == "gems/dbGems":
			DB.newPlayer(ID, destination, "gems/gemsTemplate")
			DB.updateField(ID, "ID", ID, destination)
			DB.updateField(ID, "com_time", DB.valueAt(ID, "com_time", source), destination)
			DB.updateField(ID, "gems", DB.valueAt(ID, "gems", source), destination)
			DB.updateField(ID, "inventory", DB.valueAt(ID, "inventory", source), destination)
			DB.updateField(ID, "durabilite", DB.valueAt(ID, "durabilite", source), destination)
			DB.updateField(ID, "trophy", DB.valueAt(ID, "trophy", source), destination)
			DB.updateField(ID, "daily", DB.valueAt(ID, "daily", source), destination)
			DB.updateField(ID, "banque", DB.valueAt(ID, "banque", source), destination)
			DB.updateField(ID, "hothouse", DB.valueAt(ID, "hothouse", source), destination)
			DB.updateField(ID, "cooked", DB.valueAt(ID, "cooked", source), destination)
			#DB.updateField(ID, "capability", DB.valueAt(ID, "capability", source), destination)

		i += 1
	return True
