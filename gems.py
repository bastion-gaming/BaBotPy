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

data = sqlite3.connect('players.db')
c = data.cursor()
# on ouvre la base de donnée une fois au lancement du Bot

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

def pay (ctx,nom,gain):
	"""| pay [nom] [gain] |\n donner de l'argent à vos amis ! """
	ID = ctx.message.author.id
	if spam(ID,couldown_l):
		try:
			gain = int(gain)
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
		except ValueError:
			msg = "la commande est mal formulée"
			pass
	else:
		msg = "il faut attendre "+str(couldown_l)+" secondes entre chaque commande !"
	return( ctx.message.channel.send(msg))
