import random as r
import time as t
import sqlite3

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

<<<<<<< HEAD
TOKEN = open("token","r").read().replace('\n','')
# ************** Bastion's Gems
# ************** Bot_RPG
# le token permet de reconnaitre mon bot
prefix = open("prefix.txt","r").read().replace('\n','')
# on récupère le prefix dans un fichier
client = commands.Bot(command_prefix = "{0}".format(prefix))
# on ouvre la base de donnée une fois au lancement du Bot

@client.event  # event decorator/wrapper. More on decorators here: https://pythonprogramming.net/decorators-intermediate-python-tutorial/
async def on_ready():  # method expected by client. This runs once when connected
    print(f'BastionBot | Gems Module | >> Connecté !')  # notification of login.
=======
data = sqlite3.connect('players.db')
c = data.cursor()
# on ouvre la base de donnée une fois au lancement du Bot
>>>>>>> e991f4739317d2a2b62346f29df062046352b774

def spam(ID,couldown):
	c.execute("""SELECT time FROM donnees WHERE ID=?""", (ID,))
	time = c.fetchone()
	# on récupère le la date de la dernière commande
	return(time[0] < t.time()-couldown)

def begin(ctx):
	"""permet d'initialiser la bdd, nécessaire pour pouvoir utiliser le bot """
	ID = ctx.message.author.id
	c.execute("""SELECT ID FROM donnees WHERE ID=?""", (ID,))
	rep = c.fetchone()
	if rep != None :
		msg = "personnage déjà créé !"
	else :
		gem = 10
		time = t.time()-anti_spam
		c.execute("""INSERT INTO donnees VALUES(?,?,?)""",(ID,gem,time))
		# on injecte 3 données l'ID discord, le nombre de gems,et la date de
		# la dernière commande, qui permet de vérifier de faire mon anti spam
		c.execute("""INSERT INTO inventaire VALUES(?,?,?,?,?,?,?,?,?,?,?)""",(ID,0,0,0,0,0,0,0,0,0,0))
		data.commit()
		msg = "fiche personnage créé !"
	return( ctx.message.channel.send(msg))

def prefix(ctx,gprefix):
	"""permet de changer de préfix, utilisable uniquement par certaine personne. Il est necessaire de redemarrer le bot après. """
	ID = ctx.message.author.id
	if ID == 141883318915301376 or ID ==130454275699507201 or ID == 129362501187010561 :
	#        shelll                     gnouf                        azer
		f_prefix = open("prefix.txt","w")
		f_prefix.write(gprefix)
		f_prefix.close()
		global client
		client = commands.Bot(command_prefix = "{0}".format(gprefix))
		# ne marche pas pour l'instant
		msg = "le prefix est désomrais {0}".format(gprefix)
	else :
		msg = "tu n'es pas autorisé à faire ça"
	return( ctx.message.channel.send(msg))

def crime(ctx):
	"""commets un crime et gagne des gems !"""
	ID = ctx.message.author.id
	if spam(ID,couldown_l):
	# si 10 sec c'est écoulé depuis alors on peut en  faire une nouvelle
		gain = r.randint(5,10)
		msg = message_crime[r.randint(0,3)]+str(gain)+":gem:"
		c.execute("""UPDATE donnees SET gem = gem + ? WHERE ID = ?""",(gain,ID))
		c.execute("""UPDATE donnees SET time = ? WHERE ID = ?""",(t.time(),ID))
		data.commit()
	else:
		msg = "il faut attendre "+str(couldown_l)+" secondes entre chaque commande !"
	return( ctx.message.channel.send(msg))

def bal(ctx):
	"""êtes vous riche ou pauvre ? bal vous le dit """
	ID = ctx.message.author.id
	if spam(ID,couldown_c):
		c.execute("""UPDATE donnees SET time = ? WHERE ID = ?""",(t.time(),ID))
		data.commit()
		c.execute("""SELECT gem FROM donnees WHERE ID=?""", (ID,))
		gem = c.fetchone()
		msg = "tu as actuellement : "+str(gem[0])+" :gem: !"
	else:
		msg = "il faut attendre "+str(couldown_c)+" secondes entre chaque commande !"
	return( ctx.message.channel.send(msg))

def gamble(ctx,valeur):
	"""| gamble [valeur] |\n avez vous l'ame d'un parieur ?  """
	valeur = int(valeur)
	ID = ctx.message.author.id
	if spam(ID,couldown_xl):
		if r.randint(0,3) == 0:
			gain = valeur*3
			# l'espérence est de 0 sur la gamble
			msg = message_gamble[r.randint(0,3)]+str(gain)+":gem:"
			c.execute("""UPDATE donnees SET gem = gem + ? WHERE ID = ?""",(gain,ID))
			data.commit()
		else:
			c.execute("""UPDATE donnees SET gem = gem - ? WHERE ID = ?""",(valeur,ID))
			data.commit()
			msg = "dommage tu as perdu "+str(valeur)+":gem:"
		c.execute("""UPDATE donnees SET time = ? WHERE ID = ?""",(t.time(),ID))
		data.commit()
	else:
		msg = "il faut attendre "+str(couldown_xl)+" secondes entre chaque commande !"
	return( ctx.message.channel.send(msg))

<<<<<<< HEAD
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
		DB.updateField(ID, "gems", "new_value")
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
		old = inventory[nameElem]
		inventory[nameElem] = old + nbElem
	elif nbElem >= 0:
		if nbElements(ID, nameElem) == 0:
			inventory[nameElem] = nbElem
		else :
			old = inventory[nameElem]
			inventory[nameElem] = old + nbElem
	else:
		print("On ne peut pas travailler des élements qu'il n'y a pas !")
		return 404


async def crime(ctx):
    """commets un crime et gagne des gems !"""
    ID = ctx.message.author.id
    if spam(ID,couldown_l):
        # si 10 sec c'est écoulé depuis alors on peut en  faire une nouvelle
        gain = r.randint(5,10)
        msg = message_crime[r.randint(0,3)]+str(gain)+":gem:"
        addGems(ID, gain)
        DB.updateComTime(ID)
    else:
        msg = "il faut attendre "+str(couldown_l)+" secondes entre chaque commande !"
=======
def buy (ctx,item,nb):
	"""permet d'acheter une pioche"""
	ID = ctx.message.author.id
	if spam(ID,couldown_l):
		nb = int(nb)
		c.execute("""UPDATE donnees SET gem = gem - ? WHERE ID = ?""",(20*nb,ID))
		c.execute("""UPDATE inventaire SET pickaxe = pickaxe + ? WHERE ID = ?""",(nb,ID))
		data.commit()
		msg = "tu as désormais {0} pioche.s en plus !".format(nb)
	else :
		msg = "il faut attendre "+str(couldown_l)+" secondes entre chaque commande !"
	return( ctx.message.channel.send(msg))

def mine (ctx):
	""" minez compagnons !! vous pouvez récuperer 1 à 2 cobblestone.s ou 1 d'iron"""
	ID = ctx.message.author.id
	if spam(ID,couldown_l):
		c.execute("""SELECT pickaxe FROM inventaire WHERE ID=?""", (ID,))
		if c.fetchone()[0] >= 1:
			if r.randint(0,19)==0:
				c.execute("""UPDATE inventaire set pickaxe = pickaxe - ? WHERE ID=?""", (1,ID))
				data.commit()
				msg = "pas de chance tu as cassé ta pioche !"
			else :
				if r.randint(0,7)==0:
					c.execute("""UPDATE inventaire set iron = iron + ? WHERE ID=?""", (1,ID))
					data.commit()
					msg = "tu as obtenue un bloc de iron !"
				else:
					c.execute("""UPDATE inventaire set cobblestone = cobblestone + ? WHERE ID=?""", (r.randint(1,2),ID))
					data.commit()
					msg = "tu as obtenue un bloc.s de cobblestone.s !"
		else:
			msg = "il faut acheter une pioche !"
		c.execute("""UPDATE donnees SET time = ? WHERE ID = ?""",(t.time(),ID))
		data.commit()
	else:
		msg = "il faut attendre "+str(couldown_l)+" secondes entre chaque commande !"
	return( ctx.message.channel.send(msg))

def inv (ctx):
	"""permet de voir ce que vous avez dans le ventre !"""
	ID = ctx.message.author.id
	if spam(ID,couldown_c):
		c.execute("""UPDATE donnees SET time = ? WHERE ID = ?""",(t.time(),ID))
		data.commit()
		c.execute("""SELECT pickaxe,cobblestone,iron,gold,diamond FROM inventaire WHERE ID=?""", (ID,))
		inv = c.fetchone()
		print (inv)
		msg = "**ton inventaire**\n```-pickaxe.s : "+str(inv[0])+"\n-cobblestone.s : "+str(inv[1])+"\n-iron.s : "+str(inv[2])+"\n-gold: "+str(inv[3])+"\n-diamond : "+str(inv[4])+"```"
	else:
		msg = "il faut attendre "+str(couldown_c)+" secondes entre chaque commande !"
	return( ctx.message.channel.send(msg))
>>>>>>> e991f4739317d2a2b62346f29df062046352b774

def sell (ctx,item,nb):
	"""| sell [item] [nombre] |\nLes valeurs d'échange :\ncobblestone => 1\niron => 10"""
	ID = ctx.message.author.id
	if spam(ID,couldown_l):
		try :
			nb = int(nb)
			mult = 0
			if item == "cobblestone":
				mult = 1
			elif item =="iron":
				mult = 10
			elif item =="gold":
				mult = 25
			elif item =="diamond":
				mult = 50
			else:
				mult = 0
			if mult != 0 :
				c.execute("""SELECT {0} FROM inventaire WHERE ID=?""".format(item), (ID,))
				a = c.fetchone()
				print(a[0])
				if int(nb) <= int(a[0]):
					gain = int(nb)*mult
					c.execute("""UPDATE inventaire SET {0} = {0} - {1} WHERE ID =? """.format(item,nb),(ID,))
					c.execute("""UPDATE donnees SET gem = gem + ? WHERE ID=?""",(gain,ID))
					data.commit()
					msg = "tu as vendu {0} {1} pour {2} :gem:".format(nb,item,gain)
				else :
					msg = "tu n'as pas assez de {0} pour ça !".format(item)
			else:
				msg = "commande mal remplis (item)"
		except ValueError:
			msg = "commande mal remplis (nombre)"
			pass
	else:
		msg = "il faut attendre "+str(couldown_l)+" secondes entre chaque commande !"
	return( ctx.message.channel.send(msg))

<<<<<<< HEAD

async def bal(ctx):
    """êtes vous riche ou pauvre ? bal vous le dit """
    ID = ctx.message.author.id
    if spam(ID,couldown_c):
        DB.updateField(ID, "com_time", t.time())
        gem = DB.valueAt(ID, "gems")
        msg = "tu as actuellement : "+str(gem)+" :gem: !"
        DB.updateComTime(ID)
    else:
        msg = "il faut attendre "+str(couldown_c)+" secondes entre chaque commande !"
    await ctx.message.channel.send(msg)



async def gamble(ctx,valeur):
	"""| gamble [valeur] |\n avez vous l'ame d'un parieur ?  """
	valeur = int(valeur)
	ID = ctx.message.author.id
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
	await ctx.message.channel.send(msg)



async def buy (ctx,item,nb):
	"""permet d'acheter une pioche"""
	ID = ctx.message.author.id
	if spam(ID,couldown_l):
		nb = int(nb)
		prix = 0 - (20*nb)
		addGems(ID, prix)
		addInv(ID, "pickaxe", nb)
		msg = "tu as désormais {0} pioche.s en plus !".format(nb)
	else :
		msg = "il faut attendre "+str(couldown_l)+" secondes entre chaque commande !"
	await ctx.message.channel.send(msg)


async def mine (ctx):
	""" minez compagnons !! vous pouvez récuperer 1 à 2 cobblestone.s ou 1 d'iron"""
	ID = ctx.message.author.id
	if spam(ID,couldown_l):
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
	await ctx.message.channel.send(msg)


async def inv (ctx):
	"""permet de voir ce que vous avez dans le ventre !"""
	ID = ctx.message.author.id
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
	await ctx.message.channel.send(msg)



async def sell (ctx,item,nb):
	"""| sell [item] [nombre] |\nLes valeurs d'échange :\ncobblestone => 1\niron => 10"""
	#cobble 1, iron 10, gold 50, diams 100
	ID = ctx.message.author.id
	if spam(ID,couldown_l):
		if nbElements(ID, item) >= nb:
			Tnb = 0 - nb
			addInv(ID, item, Tnb)
			if item == "cobblestone":
				gain = 1
			elif item == "iron":
				gain = r.randint(9,11)
			elif item == "gold":
				gain = r.randint(45, 56)
			elif item == "diamond":
				gain = r.randint(98, 120)
			addGems(ID, gain)
		else:
			print("Pas assez d'élement")
			msg = "Vous n'avez pas assez de "+str(item)+" il vous en reste : "+ str(nbElem(ID, item))
		DB.updateComTime(ID)
	else:
		msg = "il faut attendre "+str(couldown_l)+" secondes entre chaque commande !"
	await ctx.message.channel.send(msg)

async def pay (ctx,nom,gain):
=======
def pay (ctx,nom,gain):
>>>>>>> e991f4739317d2a2b62346f29df062046352b774
	"""| pay [nom] [gain] |\n donner de l'argent à vos amis ! """
	ID = ctx.message.author.id
	if spam(ID,couldown_l):
		try:
			gain = int(gain)
<<<<<<< HEAD
			if len(nom) == 21 :
				ID_recu = nom[2:20]
			elif len(nom) == 22 :
				ID_recu = nom[3:21]
			else :
				ID_recu = "une autre erreur ?"
			Tgain = 0 - gain
			if addGems(ID, Tgain) >= 0:
				addGems(ID_recu, gain)
				msg = "<@{0}> donne {1}:gem: à <@{2}> !".format(ID,gain,ID_recu)
			else:
				msg = "<@{0}> n'a pas assez pour donner à <@{2}> !".format(ID,gain,ID_recu)
			DB.updateComTime(ID)
=======
			if gain > 0:
				if len(nom) == 21 :
					ID_recu = nom[2:20]
				elif len(nom) == 22 :
					ID_recu = nom[3:21]
				else :
					ID_recu = "une autre erreur ?"
				c.execute("""UPDATE donnees SET gem = gem - ? WHERE ID = ? """,(gain,ID))
				c.execute("""UPDATE donnees SET gem = gem + ? WHERE ID = ? """,(gain,ID_recu))
				data.commit()
				msg = "<@{0}> donne {1}:gem: à <@{2}> !".format(ID,gain,ID_recu)
			else:
				msg = "il faut une valeur strictement supérieur à 0 !"
>>>>>>> e991f4739317d2a2b62346f29df062046352b774
		except ValueError:
			msg = "la commande est mal formulée"
			pass
	else:
		msg = "il faut attendre "+str(couldown_l)+" secondes entre chaque commande !"
<<<<<<< HEAD
	await ctx.message.channel.send(msg)
=======
	return( ctx.message.channel.send(msg))
>>>>>>> e991f4739317d2a2b62346f29df062046352b774
