import discord
from tinydb import TinyDB, Query
from tinydb.operations import delete
import datetime as dt
import time as t
import json


DB_NOM = 'bastionDB.json'

def dbExist():
	"""
	Retourne True ou False en fonction de si la db existe.
	"""
	try:
		with open(DB_NOM): pass
	except IOError:
		return False
	return True

db = TinyDB(DB_NOM)
file = "fieldTemplate.json"

def fieldList():
	with open(file, "r") as f:
		t = json.load(f)
	return t

def DBFieldList():
	D = db
	L=dict()
	E=dict()
	for x in D:
		for y in x:
			E={y:x[y]}
			L.update(E)
	return L

def checkField():
	"""
	Va vérifier que la base de donnée est à jour par rapport au fichier fieldTemplate.
	Si il découvre un champ qui n'exsite pas, alors il met à jour.
	"""
	flag = 0
	FL = fieldList() #Liste du template
	DBFL = DBFieldList() #Liste des champs actuellement dans la DB
	#Ajout
	for x in FL:
		if db.search(Query()[x]) == []:
			db.update({str(x):FL[x]})
			DBFL.clear()
			DBFL = DBFieldList() #Liste des champs actuellement dans la DB
			flag = "add"+str(flag)

	#Supression
	for x in DBFL:
		if x not in FL:
			db.update(delete(x))
			DBFL.clear()
			DBFL = DBFieldList() #Liste des champs actuellement dans la DB
			flag = "sup"+str(flag)

	#Type
	for x in DBFL:
		if not isinstance(DBFL[x],type(FL[x])):
			db.update({str(x):FL[x]})
			flag = "type"+str(flag)

	return flag

def newPlayer(ID):
	"""
	Permet d'ajouter un nouveau joueur à la base de donnée en fonction de son ID.

	ID: int de l'ID du joueur
	"""
	FieldsL = fieldList()
	if db.search(Query().ID == ID) == []:
		#Init du joueur avec les champs de base
		db.insert(fieldList())
		updateField(FieldsL["ID"], "ID", ID)
		return ("Le joueur a été ajouté !")
	else:
		return ("Le joueur existe déjà")


def updateField(ID, fieldName, fieldValue):
	"""
	Permet de mettre à jour la valeur fieldName par la fieldValue.

	ID: int de l'ID du joueur.
	fieldName: string du nom du champ à changer
	fieldValue: string qui va remplacer l'ancienne valeur
	"""
	if db.search(getattr(Query(),fieldName)) == []:
		print("Le champ n'existe pas")
		return "201"
	else:
		db.update({fieldName: fieldValue}, Query().ID == ID)
		print("Le champ a été mis à jour")
		return "200"


def valueAt(ID, fieldName):
	"""
	Permet de récupérer la valeur contenue dans le champ fieldName de ID

	ID: int de l'ID du joueur
	fieldName: string du nom du champ à chercher
	"""
	return db.search(Query().ID == ID)[0][fieldName]

async def count(message):
	l=len(db)
	if l == 0:
		await message.channel.send('Aucun utilisaeur enregistrer dans la BDD')
	else:
		await message.channel.send('{l} utilisateur inscrit')
	return l

def taille():
	return len(db)

def userID(i):
	return db.search(Query().ID)[i]["ID"]

def userGems(i):
	return db.search(Query().gems)[i]["gems"]

def updateComTime(ID, nameElem):
	"""
	Met à jour la date du dernier appel à une fonction
	"""
	ComTime = db.search(Query().ID == ID)[0]["com_time"]
	ComTime[nameElem] = t.time()
	updateField(ID, "com_time", ComTime)
