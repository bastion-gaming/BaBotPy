import random as r
import time as t
import DB

message_crime = ["You robbed the Society of Schmoogaloo and ended up in a lake,but still managed to steal ",
"tu as volé une pomme qui vaut ", "tu as gangé le loto ! prends tes ", "j'ai plus d'idée prends ça "]
# 4 phrases
message_gamble = ["tu as remporté le pari ! tu obtiens ","Une grande victoire pour toi ! tu gagnes ",
"bravo prends ", "heu.... "]
# 4 phrases
# se sont les phrases prononcé par le bot pour plus de diversité
couldown_xl = 16
couldown_l = 8 # l pour long
couldown_c = 4 # c pour court
# nb de sec nécessaire entre 2 commandes

def spam(ID,couldown):
	time = DB.valueAt(ID, "com_time")
	# on récupère le la date de la dernière commande
	return(time < t.time()-couldown)

def addGems(ID, nbGems):
	"""
	Permet d'ajouter un nombre de gems à quelqu'un. Il nous faut son ID et le nombre de gems.
	Si vous souhaitez en retirer mettez un nombre négatif.
	Si il n'y a pas assez d'argent sur le compte la fonction retourne un nombre
	strictement inférieur à 0.
	"""
	old_value = DB.valueAt(ID, "gems")
	new_value = int(old_value) + nbGems
	if new_value >= 0:
		DB.updateField(ID, "gems", new_value)
		print("Le compte de "+str(ID)+ " est maintenant de: "+str(new_value))
	else:
		print("Il n'y a pas assez sur ce compte !")
	return str(new_value)

def nbElements(ID, nameElem):
	"""
	Permet de savoir combien il y'a de nameElem dans l'inventaire de ID
	"""
	inventory = DB.valueAt(ID, "inventory")
	if nameElem in inventory:
		return inventory[nameElem]
	else:
		return 0

def addInv(ID, nameElem, nbElem):
	"""
	Permet de modifier le nombre de nameElem pour ID
	Pour en retirer mettez nbElemn en négatif
	"""
	inventory = DB.valueAt(ID, "inventory")
	if nbElements(ID, nameElem) > 0 and nbElem < 0:
		inventory[nameElem] += nbElem
	elif nbElem >= 0:
		if nbElements(ID, nameElem) == 0:
			inventory[nameElem] = nbElem
		else :
			inventory[nameElem] += nbElem
	else:
		print("On ne peut pas travailler des élements qu'il n'y a pas !")
		return 404
	DB.updateField(ID, "inventory", inventory)

def begin(ctx):
	ID = ctx.author.id
	return(ctx.channel.send(DB.newPlayer(ID)))

def crime(ctx):
	"""commets un crime et gagne des gems !"""
	ID = ctx.author.id
	if spam(ID,couldown_l):
		# si 10 sec c'est écoulé depuis alors on peut en  faire une nouvelle
		gain = r.randint(5,10)
		msg = message_crime[r.randint(0,3)]+str(gain)+":gem:"
		addGems(ID, gain)
		DB.updateComTime(ID)
	else:
		msg = "il faut attendre "+str(couldown_l)+" secondes entre chaque commande !"

	return (ctx.channel.send(msg))


def bal(ctx):
	"""êtes vous riche ou pauvre ? bal vous le dit """
	ID = ctx.author.id
	if spam(ID,couldown_c):
		DB.updateField(ID, "com_time", t.time())
		gem = DB.valueAt(ID, "gems")
		msg = "tu as actuellement : "+str(gem)+" :gem: !"
		DB.updateComTime(ID)
	else:
		msg = "il faut attendre "+str(couldown_c)+" secondes entre chaque commande !"
	return (ctx.channel.send(msg))



def gamble(ctx,valeur):
	"""| gamble [valeur] |\n avez vous l'ame d'un parieur ?  """
	valeur = int(valeur)
	ID = ctx.author.id
	if spam(ID,couldown_xl):
		if r.randint(0,3) == 0:
			gain = valeur*3
			# l'espérence est de 0 sur la gamble
			msg = message_gamble[r.randint(0,3)]+str(gain)+":gem:"
			addGems(ID, gain)
		else:
			val = 0-valeur
			addGems(ID,val)
			msg = "dommage tu as perdu "+str(valeur)+":gem:"
		DB.updateComTime(ID)
	else:
		msg = "il faut attendre "+str(couldown_xl)+" secondes entre chaque commande !"
	return(ctx.channel.send(msg))



def buy (ctx,item,nb):
	"""permet d'acheter une pioche"""
	ID = ctx.author.id
	if spam(ID,couldown_l):
		nb = int(nb)
		prix = 0 - (20*nb)
		addGems(ID, prix)
		addInv(ID, "pickaxe", nb)
		msg = "tu as désormais {0} pioche.s en plus !".format(nb)
	else :
		msg = "il faut attendre "+str(couldown_l)+" secondes entre chaque commande !"
	return (ctx.channel.send(msg))


def mine (ctx):
	""" minez compagnons !! vous pouvez récuperer 1 à 2 cobblestone.s ou 1 d'iron"""
	ID = ctx.author.id
	if spam(ID,couldown_l):
		print(nbElements(ID, "pickaxe"))
		if nbElements(ID, "pickaxe") >= 1:
			if r.randint(0,19)==0:
				addInv(ID,"pickaxe," -1)
				msg = "pas de chance tu as cassé ta pioche !"
			else :
				if r.randint(0,7)==0:
					addInv(ID, "iron", 1)
					msg = "tu as obtenue un bloc de iron !"
				else:
					addInv(ID, "cobblestone", 1)
					msg = "tu as obtenue un bloc.s de cobblestone.s !"
		else:
			msg = "il faut acheter une pioche !"
		DB.updateComTime(ID)
	else:
		msg = "il faut attendre "+str(couldown_l)+" secondes entre chaque commande !"
	return (ctx.channel.send(msg))


def inv (ctx):
	"""permet de voir ce que vous avez dans le ventre !"""
	ID = ctx.author.id
	if spam(ID,couldown_c):
		inv = DB.valueAt(ID, "inventory")
		print (inv)
		msg="**ton inventaire**\n```"
		for x in inv:
			msg = msg+"- "+str(x)+": "+str(inv[x])+"\n"
		msg = msg +"```"
		#msg = "**ton inventaire**\n```-pickaxe.s : "+str(inv[0])+"\n-cobblestone.s : "+str(inv[1])+"\n-iron.s : "+str(inv[2])+"\n-gold: "+str(inv[3])+"\n-diamond : "+str(inv[4])+"```"
		DB.updateComTime(ID)
	else:
		msg = "il faut attendre "+str(couldown_c)+" secondes entre chaque commande !"
	return (ctx.channel.send(msg))

def sell (ctx,item,nb):
	"""| sell [item] [nombre] |\nLes valeurs d'échange :\ncobblestone => 1\niron => 10"""
	#cobble 1, iron 10, gold 50, diams 100
	ID = ctx.author.id
	if spam(ID,couldown_l):
		nb = int(nb)
		if nbElements(ID, item) >= nb:
			addInv(ID, item, -nb)
			if item == "cobblestone":
				coef = 1
			elif item == "iron":
				coef = r.randint(9,11)
			elif item == "gold":
				coef = r.randint(45, 56)
			elif item == "diamond":
				coef = r.randint(98, 120)
			gain = coef*nb
			addGems(ID, gain)
			msg ="tu as vendu {} {} pour {} :gem: !".format(nb,item,gain)
		else:
			print("Pas assez d'élement")
			msg = "Vous n'avez pas assez de "+str(item)+" il vous en reste : "+ str(nbElements(ID, item))
		DB.updateComTime(ID)
	else:
		msg = "il faut attendre "+str(couldown_l)+" secondes entre chaque commande !"
	return (ctx.channel.send(msg))

def pay (ctx,nom,gain):
	"""| pay [nom] [gain] |\n donner de l'argent à vos amis ! """
	ID = ctx.author.id
	if spam(ID,couldown_l):
		try:
			gain = int(gain)
			don = -gain
			if len(nom) == 21 :
				ID_recu = int(nom[2:20])
			elif len(nom) == 22 :
				ID_recu = int(nom[3:21])
			else :
				ID_recu = "une autre erreur ?"
			if int(DB.valueAt(ID, "gems")) >= 0:
				print(ID_recu)
				addGems(ID_recu, gain)
				addGems(ID,don)
				msg = "<@{0}> donne {1}:gem: à <@{2}> !".format(ID,gain,ID_recu)
			else:
				msg = "<@{0}> n'a pas assez pour donner à <@{2}> !".format(ID,gain,ID_recu)
			DB.updateComTime(ID)
		except ValueError:
			msg = "la commande est mal formulée"
			pass
	else:
		msg = "il faut attendre "+str(couldown_l)+" secondes entre chaque commande !"
	return (ctx.channel.send(msg))
