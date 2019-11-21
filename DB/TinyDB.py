import discord
from tinydb import TinyDB, Query
from tinydb.operations import delete
import datetime as dt
import time as t
import json
from core import welcome as wel
from gems import gemsFonctions as GF


DB_NOM = 'bastionDB'

def dbExist(linkDB = None):
	"""
	Retourne True ou False en fonction de si la db existe.
	"""
	try:
		if linkDB != None:
			with open("{}.json".format(linkDB)): pass
		else:
			with open("DB/{}.json".format(DB_NOM)): pass
	except IOError:
		if linkDB != None:
			db = TinyDB("{}.json".format(linkDB))
			db.close()
		return False
	return True

#-------------------------------------------------------------------------------
def fieldList(file):
	with open("{}.json".format(file), "r") as f:
		t = json.load(f)
	return t

def DBFieldList(linkDB = None):
	if linkDB != None:
		db = TinyDB("{}.json".format(linkDB))
	else:
		db = TinyDB("DB/{}.json".format(DB_NOM))
	D = db
	L=dict()
	E=dict()
	for x in D:
		for y in x:
			E={y:x[y]}
			L.update(E)
	db.close()
	return L

#-------------------------------------------------------------------------------
def checkField(linkDB, linkfield):
	"""
	Va vérifier que la base de donnée est à jour par rapport au fichier fieldTemplate.
	Si il découvre un champ qui n'exsite pas, alors il met à jour.
	"""
	db = TinyDB("{}.json".format(linkDB))
	flag = 0
	FL = fieldList(linkfield) #Liste du template
	DBFL = DBFieldList(linkDB) #Liste des champs actuellement dans la DB
	#Ajout
	for x in FL:
		if db.search(Query()[x]) == []:
			db.update({str(x):FL[x]})
			DBFL.clear()
			DBFL = DBFieldList(linkDB) #Liste des champs actuellement dans la DB
			flag = "add"+str(flag)

	#Supression
	for x in DBFL:
		if x not in FL:
			db.update(delete(x))
			DBFL.clear()
			DBFL = DBFieldList(linkDB) #Liste des champs actuellement dans la DB
			flag = "sup"+str(flag)

	#Type
	for x in DBFL:
		if not isinstance(DBFL[x],type(FL[x])):
			db.update({str(x):FL[x]})
			flag = "type"+str(flag)

	db.close()
	return flag

#===============================================================================
# Gestion des utilisateurs
#===============================================================================
def newPlayer(ID, linkDB = None, linkfield = None):
	"""
	Permet d'ajouter un nouveau joueur à la base de donnée en fonction de son ID.

	ID: int de l'ID du joueur
	"""
	if linkDB != None:
		db = TinyDB("{}.json".format(linkDB))
	else:
		db = TinyDB("DB/{}.json".format(DB_NOM))
	if linkfield == None:
		linkfield = "DB/fieldTemplate"
	FieldsL = fieldList(linkfield)
	if db.search(Query().ID == ID) == []:
		#Init du joueur avec les champs de base
		db.insert(fieldList(linkfield))
		updateField(FieldsL["ID"], "ID", ID, linkDB)
		db.close()
		return ("Le joueur a été ajouté !")
	else:
		db.close()
		return ("Le joueur existe déjà")

#-------------------------------------------------------------------------------
def removePlayer(ID, linkDB = None):
	if linkDB != None:
		db = TinyDB("{}.json".format(linkDB))
	else:
		db = TinyDB("DB/{}.json".format(DB_NOM))
	el = db.get(Query().ID == ID)
	docID = el.doc_id
	try:
		db.remove(doc_ids=[docID])
		print("DB >> docID {} | Le joueur {} a été supprimer de la DB".format(docID, ID))
		db.close()
		return ("Le joueur a été supprimer !")
	except:
		db.close()
		return ("Le joueur n'existe pas")

#-------------------------------------------------------------------------------
def membercheck(ctx):
	"""
	Pour chaque joueur de la DB, vérifie si il est présent sur le serveur Bastion.
	Si il ne l'es plus, la fonction supprime le joueur de la DB.
	"""
	t = taille()
	i = 1
	if ctx.guild == wel.idBASTION:
		while i < t:
			try:
				ID = userID(i)
				if ctx.guild.get_member(ID) == None:
					removePlayer(ID)
				i += 1
			except:
				return True
		return False
	else:
		return 404

#===============================================================================
# Compteur
#===============================================================================
def countTotalMsg(linkDB = None):
	#Init a
	a=0
	if linkDB != None:
		db = TinyDB("{}.json".format(linkDB))
	else:
		db = TinyDB("DB/{}.json".format(DB_NOM))
	for item in db:
#On additionne le nombre de message posté en tout
		a = a + int(item["nbMsg"])
	db.close()
	return a

#-------------------------------------------------------------------------------
def countTotalGems(linkDB = None):
	#Init a
	a=0
	if linkDB != None:
		db = TinyDB("{}.json".format(linkDB))
	else:
		db = TinyDB("DB/{}.json".format(DB_NOM))
	for item in db:
#On additionne le nombre de message posté en tout
		a = a + int(item["gems"])
	db.close()
	return a


#===============================================================================
# Fonctions
#===============================================================================

def updateField(ID, fieldName, fieldValue, linkDB = None):
	"""
	Permet de mettre à jour la valeur fieldName par la fieldValue.

	ID: int de l'ID du joueur.
	fieldName: string du nom du champ à changer
	fieldValue: string qui va remplacer l'ancienne valeur
	"""
	if linkDB != None:
		db = TinyDB("{}.json".format(linkDB))
	else:
		db = TinyDB("DB/{}.json".format(DB_NOM))
	if db.search(getattr(Query(),fieldName)) == []:
		# print("DB >> Le champ n'existe pas")
		db.close()
		return "201"
	else:
		db.update({fieldName: fieldValue}, Query().ID == ID)
		# print("DB >> Le champ a été mis à jour")
		db.close()
		return "200"

#-------------------------------------------------------------------------------
def valueAt(ID, fieldName, linkDB = None):
	"""
	Permet de récupérer la valeur contenue dans le champ fieldName de ID

	ID: int de l'ID du joueur
	fieldName: string du nom du champ à chercher
	"""
	if linkDB != None:
		db = TinyDB("{}.json".format(linkDB))
	else:
		db = TinyDB("DB/{}.json".format(DB_NOM))
	value = db.search(Query().ID == ID)[0][fieldName]
	db.close()
	return value

#-------------------------------------------------------------------------------
def taille(linkDB = None):
	"""Retourne la taille de la DB"""
	if linkDB != None:
		db = TinyDB("{}.json".format(linkDB))
	else:
		db = TinyDB("DB/{}.json".format(DB_NOM))
	t = len(db)
	db.close()
	return t

#-------------------------------------------------------------------------------
def userID(i, linkDB = None):
	if linkDB != None:
		db = TinyDB("{}.json".format(linkDB))
	else:
		db = TinyDB("DB/{}.json".format(DB_NOM))
	ID = db.search(Query().ID)[i]["ID"]
	db.close()
	return ID

#-------------------------------------------------------------------------------
def get_endDocID(linkDB = None):
	if linkDB != None:
		db = TinyDB("{}.json".format(linkDB))
	else:
		db = TinyDB("DB/{}.json".format(DB_NOM))
	el = db.all()[taille(linkDB)-1]
	IDi = el.doc_id
	db.close()
	return IDi

#-------------------------------------------------------------------------------
def userExist(ID, linkDB = None):
	if linkDB != None:
		db = TinyDB("{}.json".format(linkDB))
	else:
		db = TinyDB("DB/{}.json".format(DB_NOM))
	if db.search(Query().ID == ID) == []:
		db.close()
		return False
	else :
		db.close()
		return True

#-------------------------------------------------------------------------------
def OwnerSessionExist(value, linkDB = None):
	"""
	Vérifie l'existance d'une session créée par Owner
	"""
	if linkDB != None:
		db = TinyDB("{}.json".format(linkDB))
	else:
		return 404
	if db.search(Query().owner == value) == []:
		db.close()
		return False
	else :
		db.close()
		return True

#-------------------------------------------------------------------------------
def MemberSessionExist(value, linkDB = None):
	"""
	Vérifie l'existance d'une session créée par Owner
	"""
	if linkDB != None:
		db = TinyDB("{}.json".format(linkDB))
	else:
		return 404
	temp = []
	temp.append(value)
	if db.search(Query().member == temp) == []:
		db.close()
		return False
	else :
		db.close()
		return True

#-------------------------------------------------------------------------------
def OwnerSessionAt(owner, fieldName, linkDB = None):
	"""
	Retourne le code session (ID) créé par Owner
	"""
	if linkDB != None:
		db = TinyDB("{}.json".format(linkDB))
	else:
		return 404
	value = db.search(Query().owner == owner)[0][fieldName]
	db.close()
	return value

#-------------------------------------------------------------------------------
def MemberSessionAt(member, fieldName, linkDB = None):
	"""
	Retourne le code session (ID) créé par Owner
	"""
	if linkDB != None:
		db = TinyDB("{}.json".format(linkDB))
	else:
		return 404
	temp = []
	temp.append(member)
	value = db.search(Query().member == temp)[0][fieldName]
	db.close()
	return value

#-------------------------------------------------------------------------------
def userGems(i, item, linkDB = None):
	"""Retourne le nombre de gems du joueur i"""
	if linkDB != None:
		db = TinyDB("{}.json".format(linkDB))
	else:
		db = TinyDB("DB/{}.json".format(DB_NOM))
	if item == "gems":
		gems = db.search(Query().gems)[i]["gems"]
	elif item == "spinelles":
		gems = db.search(Query().spinelles)[i]["spinelles"]
	db.close()
	return gems

#-------------------------------------------------------------------------------
def updateComTime(ID, nameElem, linkDB = None):
	"""
	Met à jour la date du dernier appel à une fonction
	"""
	if linkDB != None:
		db = TinyDB("{}.json".format(linkDB))
	else:
		db = TinyDB("DB/{}.json".format(DB_NOM))
		linkDB = "DB/{}".format(DB_NOM)
	ComTime = db.search(Query().ID == ID)[0]["com_time"]
	ComTime[nameElem] = t.time()
	updateField(ID, "com_time", ComTime, linkDB)
	db.close()

#-------------------------------------------------------------------------------
def addGems(ID, nbGems):
	"""
	Permet d'ajouter un nombre de gems à quelqu'un. Il nous faut son ID et le nombre de gems.
	Si vous souhaitez en retirer mettez un nombre négatif.
	Si il n'y a pas assez d'argent sur le compte la fonction retourne un nombre
	strictement inférieur à 0.
	"""
	old_value = valueAt(ID, "gems", GF.dbGems)
	new_value = int(old_value) + nbGems
	if new_value >= 0:
		updateField(ID, "gems", new_value, GF.dbGems)
		print("DB >> Le compte de "+str(ID)+ " est maintenant de: "+str(new_value))
	else:
	 	print("DB >> Il n'y a pas assez sur ce compte !")
	return str(new_value)

#-------------------------------------------------------------------------------
def daily_data(ID, nameElem):
	"""Retourne les info sur le Daily de ID"""
	DailyData = valueAt(ID, "daily", GF.dbGems)
	if nameElem in DailyData:
		data = DailyData[nameElem]
	else:
		return True
	return data

#-------------------------------------------------------------------------------
def updateDaily(ID, nameElem, value):
	"""
	Met à jour les info du daily
	"""
	DailyData = valueAt(ID, "daily", GF.dbGems)
	if nameElem == "dailymult":
		DailyData[nameElem] = value
	else:
		DailyData[nameElem] = str(value)
	updateField(ID, "daily", DailyData, GF.dbGems)

#-------------------------------------------------------------------------------
def spam(ID,couldown, nameElem, linkDB = None):
	"""Antispam """
	if linkDB == None:
		linkDB = "DB/{}".format(DB_NOM)
	ComTime = valueAt(ID, "com_time", linkDB)
	if nameElem in ComTime:
		time = ComTime[nameElem]
	else:
		return True

	# on récupère la date de la dernière commande
	return(time < t.time()-couldown)

#-------------------------------------------------------------------------------
def nom_ID(nom):
	"""Convertis un nom en ID """
	if len(nom) == 21 :
		ID = int(nom[2:20])
	elif len(nom) == 22 :
		ID = int(nom[3:21])
	else :
		print("DB >> mauvais nom")
		ID = -1
	return(ID)

#-------------------------------------------------------------------------------
def nbElements(ID, stockeur, nameElem, linkDB = None):
	"""
	Permet de savoir combien il y'a de nameElem dans l'inventaire de ID
	"""
	if linkDB != None:
		Stockeur = valueAt(ID, stockeur, linkDB)
	else:
		Stockeur = valueAt(ID, stockeur)
	if nameElem in Stockeur:
		return Stockeur[nameElem]
	else:
		return 0

#-------------------------------------------------------------------------------
def add(ID, stockeur, nameElem, nbElem, linkDB = None):
	"""
	Permet de modifier le nombre de nameElem pour ID dans le stockeur (inventory | StatGems | Trophy | banque)
	Pour en retirer mettez nbElemn en négatif
	"""
	if linkDB == None:
		linkDB = "DB/bastionDB"
	Stockeur = valueAt(ID, stockeur, linkDB)
	if nbElements(ID, stockeur, nameElem, linkDB) > 0 and nbElem < 0:
		Stockeur[nameElem] += nbElem
	elif nbElem >= 0:
		if nbElements(ID, stockeur, nameElem, linkDB) == 0:
			Stockeur[nameElem] = nbElem
		else :
			Stockeur[nameElem] += nbElem
	else:
		# print("On ne peut pas travailler des élements qu'il n'y a pas !")
		return 404
	updateField(ID, stockeur, Stockeur, linkDB)
