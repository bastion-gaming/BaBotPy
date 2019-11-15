from DB import TinyDB as DB, SQLite as sql
from tinydb import TinyDB, Query
from tinydb.operations import delete
import json


def conversionBastion(nameDB):
	t = DB.taille()
	i = 1

	if nameDB == "bastion":
		linkDB = "DB/bastionDB"
		with open("DB/fieldTemplate.json", "r") as f:
			template = json.load(f)
	elif nameDB == "gems":
		linkDB = "gems/dbGems"
		with open("gems/TemplateGems.json", "r") as f:
			template = json.load(f)
		with open("gems/TemplateHotHouse.json", "r") as f:
			templateHH = json.load(f)
	else:
		return 404
	while i < t:
		check = False
		ID = DB.userID(i)
		for x in template:
			if x == "ID":
				if sql.newPlayer(ID, nameDB) != "Le joueur a été ajouté !":
					print("Le joueur existe deja!")
					check = True
			elif not check:
				print("==== {} ====".format(x))
				if x == "com_time":
					v = DB.valueAt(ID, x, linkDB)
					for y in v:
						sql.add(ID, y, v[y], "{}_{}".format(nameDB, x))
				elif x == "inventory" or x == "durabilite" or x == "trophy" or x == "StatGems":
					v = DB.valueAt(ID, x, linkDB)
					if x == "durabilite":
						x = "durability"
					x = x.lower()
					for y in v:
						sql.add(ID, y, v[y], x)
				elif x == "daily" or x == "banque":
					v = DB.valueAt(ID, x, linkDB)
					if x == "banque":
						x = "bank"
					for y in v:
						sql.updateField(ID, y, v[y], x)
				elif x == "capability":
					v = DB.valueAt(ID, x, linkDB)
					for y in v:
						print(sql.add(ID, y, 1, x))
				elif x == "filleul":
					v = DB.valueAt(ID, x, linkDB)
					x = "filleuls"
					for y in v:
						sql.add(ID, "ID_filleul", y, x)
				elif x != "arrival" or x != "com_time" or x != "filleul":
					sql.updateField(ID, x, DB.valueAt(ID, x, linkDB), nameDB)

		if nameDB == "gems" and not check:
			for x in templateHH:
				if x == "hothouse":
					v = DB.valueAt(ID, x, "gems/dbHotHouse")
					for y in v:
						y2 = y.split("_")
						y3 = int(y2[1])
						z = [v[y], "seed"]
						if y3 <= 200:
							sql.add(ID, y3, z, "hothouse")
				elif x == "cooked":
					v = DB.valueAt(ID, x, "gems/dbHotHouse")
					for y in v:
						y2 = y.split("_")
						y3 = int(y2[1])
						z = [v[y], ""]
						if y3 <= 10:
							sql.add(ID, y3, z, "cooking")
		i += 1
	return False
