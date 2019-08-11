import discord
from tinydb import TinyDB, Query
import datetime as dt
import time as t
import json


DB_NOM = 'bastionDB.json'
db = TinyDB(DB_NOM)
inv = dict()
file = "fieldTemplate.json"

def fieldList():
	with open(file, "r") as f:
		t = json.load(f)
	return t

def checkField():
	"""
	Va vérifier que la base de donnée est à jour par rapport au fichier fieldTemplate.
	Si il découvre un champ qui n'exsite pas, alors il met à jour.
	"""
	flag = 0
	dico = fieldList()
	for x in dico:
		if db.search(Query()[x]) == []:
			db.update({str(x):dico[x]})
			flag = 1
	if flag == 0:
		return 1
	else :
		return 0

def dbExist():
	"""
	Retourne True ou False en fonction de si la db existe.
	"""
	try:
		with open(DB_NOM): pass
	except IOError:
		return False
	return True

def newPlayer(ID):
	"""
	Permet d'ajouter un nouveau joueur à la base de donnée en fonction de son ID.

	ID: int de l'ID du joueur
	"""

	if db.search(Query().ID == ID) == []:
		#Init du joueur avec les champs de base
		#########################MODIFIER ICI SI NVX CHAMPS#####################
		db.insert(fieldList())
		########################################################################
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

def updateComTime(ID):
	"""
	Met à jour la date du dernier appel à une fonction
	"""
	updateField(ID, "com_time", t.time())
