import discord
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
# il n'y en a pas bcp donc je les laisse directement dans le code
anti_spam = 6
anti_spam2 = 3
# nb de sec nécessaire entre 2 commandes
client = discord.Client()
data = sqlite3.connect('players.db')
c = data.cursor()

# Au démarrage du bot.
@client.event
async def on_ready():
    print('BastionBot | Gems Module | >> Connecté !')

async def begin(message):
    ID = message.author.id
    c.execute("""SELECT ID FROM donnees WHERE ID=?""", (ID,))
    rep = c.fetchone()
    print (rep)
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
    await message.channel.send(msg)

async def crime(message):
	ID = message.author.id
	c.execute("""SELECT time FROM donnees WHERE ID=?""", (ID,))
	time = c.fetchone()
	# on récupère le la date de la dernière commande
	if time[0] < t.time()-anti_spam:
	# si 10 sec c'est écoulé depuis alors on peut en  faire une nouvelle
		gain = r.randint(5,10)
		msg = message_crime[r.randint(0,3)]+str(gain)+":gem:"
		c.execute("""UPDATE donnees SET gem = gem + ? WHERE ID = ?""",(gain,ID))
		c.execute("""UPDATE donnees SET time = ? WHERE ID = ?""",(t.time(),ID))
	else:
		msg = "il faut attendre "+str(anti_spam)+" secondes entre chaque commande !"
	await message.channel.send(msg)
	data.commit()

async def bal(message):
	ID = message.author.id
	c.execute("""SELECT time FROM donnees WHERE ID=?""", (ID,))
	time = c.fetchone()
	if time[0] < t.time()-anti_spam2:
		c.execute("""UPDATE donnees SET time = ? WHERE ID = ?""",(t.time(),ID))
		c.execute("""SELECT gem FROM donnees WHERE ID=?""", (ID,))
		gem = c.fetchone()
		msg = "tu as actuellement : "+str(gem[0])+" :gem: !"
	else:
		msg = "il faut attendre "+str(anti_spam2)+" secondes entre chaque commande !"
	await message.channel.send(msg)
	data.commit()

async def gamble(message):
	valeur = int(message.content[10:])
	ID = message.author.id
	c.execute("""SELECT time FROM donnees WHERE ID=?""", (ID,))
	time = c.fetchone()
	if time[0] < t.time()-anti_spam:
		if r.randint(0,3) == 0:
			gain = valeur*3
			# l'espérence est de 0 sur la gamble
			msg = message_gamble[r.randint(0,3)]+str(gain)+":gem:"
			c.execute("""UPDATE donnees SET gem = gem + ? WHERE ID = ?""",(gain,ID))
		else:
			c.execute("""UPDATE donnees SET gem = gem - ? WHERE ID = ?""",(valeur,ID))
			msg = "dommage tu as perdu "+str(valeur)+":gem:"
		c.execute("""UPDATE donnees SET time = ? WHERE ID = ?""",(t.time(),ID))
	else:
		msg = "il faut attendre "+str(anti_spam)+" secondes entre chaque commande !"
	await message.channel.send(msg)
	data.commit()

async def sell(message):
	ID = message.author.id
	i = 0
	content = message.content[8:]
	item,nb = content.split(" ")
	try :
		int(nb)
		mult = 0
		print(item,nb)
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
		await message.channel.send(msg)

async def pay(message):
	ID = message.author.id
	content = message.content[7:]
	nom,gain = content.split(" ")
	if len(nom) == 21 :
		ID_recu = nom[2:20]
	elif len(nom) == 22 :
		ID_recu = nom[3:21]
	else :
		ID_recu = "une autre erreur ?"
	msg = "tu veux donner : "+gain+":gem: à "+nom+" dont l'id est "+ID_recu
	print(msg)
	await message.channel.send(msg)

async def buy(message):
	ID = message.author.id
	c.execute("""UPDATE donnees SET gem = gem - ? WHERE ID = ?""",(20,ID))
	c.execute("""UPDATE inventaire SET pickaxe = pickaxe + ? WHERE ID = ?""",(1,ID))
	data.commit()
	await client.send_message(message.channel, "tu as désormais une pioche en plus !")
