import discord
from tinydb import TinyDB, Query
from tinydb.operations import delete
import datetime as dt
import time as t
import json


DB_NOM = 'DB/bastionDB.json'

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
file = "DB/fieldTemplate.json"

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

def nom_ID(nom):
	if len(nom) == 21 :
		ID = int(nom[2:20])
	elif len(nom) == 22 :
		ID = int(nom[3:21])
	else :
		print("DB >> mauvais nom")
		ID = "prout"
	return(ID)

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
	elif valueAt(ID, "arrival") == "0":
		return ("Le joueur a été ajouté !")
	else:
		return ("Le joueur existe déjà")


def removePlayer(ID):
	el = db.get(Query().ID == ID)
	docID = el.doc_id
	try:
		db.remove(doc_ids=[docID])
		print("DB >> docID {} | Le joueur {} a été supprimer de la DB".format(docID, ID))
		return ("Le joueur a été supprimer !")
	except:
		return ("Le joueur n'existe pas")


def DBmembercheck(ctx):
	t = taille()
	i = 1
	while i < t:
		try:
			id = userID(i)
			if ctx.guild.get_member(id) == None:
				removePlayer(id)
			i += 1
		except:
			return True
	return False


def updateField(ID, fieldName, fieldValue):
	"""
	Permet de mettre à jour la valeur fieldName par la fieldValue.

	ID: int de l'ID du joueur.
	fieldName: string du nom du champ à changer
	fieldValue: string qui va remplacer l'ancienne valeur
	"""
	if db.search(getattr(Query(),fieldName)) == []:
		print("DB >> Le champ n'existe pas")
		return "201"
	else:
		db.update({fieldName: fieldValue}, Query().ID == ID)
		print("DB >> Le champ a été mis à jour")
		return "200"


def valueAt(ID, fieldName):
	"""
	Permet de récupérer la valeur contenue dans le champ fieldName de ID

	ID: int de l'ID du joueur
	fieldName: string du nom du champ à chercher
	"""
	return db.search(Query().ID == ID)[0][fieldName]

def taille():
	return len(db)

def userID(i):
	return db.search(Query().ID)[i]["ID"]

def userExist(id):
	if db.search(Query().ID == id) == []:
		return False
	else :
		return True

def userGems(i):
	return db.search(Query().gems)[i]["gems"]

def updateComTime(ID, nameElem):
	"""
	Met à jour la date du dernier appel à une fonction
	"""
	ComTime = db.search(Query().ID == ID)[0]["com_time"]
	ComTime[nameElem] = t.time()
	updateField(ID, "com_time", ComTime)

def addGems(ID, nbGems):
	"""
	Permet d'ajouter un nombre de gems à quelqu'un. Il nous faut son ID et le nombre de gems.
	Si vous souhaitez en retirer mettez un nombre négatif.
	Si il n'y a pas assez d'argent sur le compte la fonction retourne un nombre
	strictement inférieur à 0.
	"""
	old_value = valueAt(ID, "gems")
	new_value = int(old_value) + nbGems
	if new_value >= 0:
		updateField(ID, "gems", new_value)
		print("DB >> Le compte de "+str(ID)+ " est maintenant de: "+str(new_value))
	else:
	 	print("DB >> Il n'y a pas assez sur ce compte !")
	return str(new_value)

def daily_data(ID, nameElem):
	DailyData = valueAt(ID, "daily")
	if nameElem in DailyData:
		data = DailyData[nameElem]
	else:
		return True
	return data

def updateDaily(ID, nameElem, value):
	"""
	Met à jour les info du daily
	"""
	DailyData = valueAt(ID, "daily")
	if nameElem == "dailymult":
		DailyData[nameElem] = value
	else:
		DailyData[nameElem] = str(value)
	updateField(ID, "daily", DailyData)

def spam(ID,couldown, nameElem):
	ComTime = valueAt(ID, "com_time")
	if nameElem in ComTime:
		time = ComTime[nameElem]
	else:
		return True

	# on récupère le la date de la dernière commande
	return(time < t.time()-couldown)

def nom_ID(nom):
	if len(nom) == 21 :
		ID = int(nom[2:20])
	elif len(nom) == 22 :
		ID = int(nom[3:21])
	else :
		print("DB >> mauvais nom")
		ID = -1
	return(ID)

def nbElements(ID, stockeur, nameElem):
	"""
	Permet de savoir combien il y'a de nameElem dans l'inventaire de ID
	"""
	Stockeur = valueAt(ID, stockeur)
	if nameElem in Stockeur:
		return Stockeur[nameElem]
	else:
		return 0


def add(ID, stockeur, nameElem, nbElem):
	"""
	Permet de modifier le nombre de nameElem pour ID dans le stockeur (inventory | StatGems | Trophy | banque)
	Pour en retirer mettez nbElemn en négatif
	"""
	Stockeur = valueAt(ID, stockeur)
	if nbElements(ID, stockeur, nameElem) > 0 and nbElem < 0:
		Stockeur[nameElem] += nbElem
	elif nbElem >= 0:
		if nbElements(ID, stockeur, nameElem) == 0:
			Stockeur[nameElem] = nbElem
		else :
			Stockeur[nameElem] += nbElem
	else:
		# print("On ne peut pas travailler des élements qu'il n'y a pas !")
		return 404
	updateField(ID, stockeur, Stockeur)
