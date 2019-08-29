import random as r
import datetime as dt
import DB
from discord.ext import commands, tasks
from discord.ext.commands import bot
from discord.utils import get
import discord
import json
import matplotlib.pyplot as plt
import os

client = discord.Client()
file="time.json"
def fileExist():
	try:
		with open(file): pass
	except IOError:
	    return False
	return True

def countCo():
	t = json.load(open("co.json","r"))
	t["co local"]+=1
	t["co total"]+=1
	with open("co.json", 'w') as f:
		f.write(json.dumps(t, indent=4))

def countDeco():
	t = json.load(open("co.json","r"))
	t["deco local"]+=1
	t["deco total"]+=1
	with open("co.json", 'w') as f:
		f.write(json.dumps(t, indent=4))

async def countMsg(message):
	id = message.author.id
	try:
		DB.updateField(id, "nbMsg", int(DB.valueAt(id, "nbMsg")+1))
	except:
		return print("Le joueur n'existe pas.")
	return print(DB.valueAt(id, "nbMsg"))

def countTotalMsg():
	#Init a
	a=0
	for item in DB.db:
#On additionne le nombre de message posté en tout
		a = a + int(item["nbMsg"])
	return a

def hourCount():
	d=dt.datetime.now().hour
	if fileExist() == False:
		t = {"0":0,"1":0,"2":0,"3":0,"4":0,"5":0,"6": 0,"7": 0,"8": 0,"9": 0,"10": 0,"11": 0,"12": 0,"13": 0,"14": 0,"15": 0,"16": 0,"17": 0,"18": 0,"19": 0,"20": 0,"21": 0,"22": 0,"23":0}
		t[str(d)]=int(countTotalMsg())
		with open(file, 'w') as f:
			f.write(json.dumps(t, indent=4))
		return d
	else:
		with open(file, "r") as f:
			t = json.load(f)
			t[str(d)]=int(countTotalMsg())
		with open(file, 'w') as f:
			f.write(json.dumps(t, indent=4))
	print("time.json modifié")

#===============================================================

class Stats(commands.Cog):

	def __init__(self,bot):
		self.hour = dt.datetime.now().hour
		self.bot = bot
		self.day = dt.date.today()
		self.hourWrite.start()
		return(None)

	def cog_unload(self):
		self.hourWrite.cancel()


	@tasks.loop(seconds=300.0)
	async def hourWrite(self):
		"""
		Va, toute les heures, écrire dans time.json le nombre total de message écrit sur le serveur.
		"""
		if self.hour != dt.datetime.now().hour :
			if self.day != dt.date.today():
				msg_total = countTotalMsg()
				local_heure={}
				f = open(file, "r")
				connexion = json.load(open("co.json", "r"))
				total_heure = json.load(open(file, "r"))
				for i in range(23):
					local_heure[str(i)] = total_heure[str(i+1)] - total_heure[str(i)]
				local_heure["23"] = msg_total - total_heure[str("23")]
				msg_jour = msg_total - total_heure["0"]
				co_local = 0
				co_total = 0
				deco_local = 0
				deco_total = 0
				nouveau_jour = {
								"msg total jour" : msg_total,
								"msg local jour" : msg_jour,
								"msg total heures" : total_heure,
								"msg local heures" :local_heure,
								"co local" : connexion["co local"],
								"co total" : connexion["co total"],
								"deco total" : connexion["deco total"],
								"deco local" : connexion["deco local"],
								"nombre de joueurs" : 120
								}
				connexion["co local"] = 0
				connexion["deco local"] = 0
				with open("co.json", 'w') as f:
					f.write(json.dumps(connexion, indent=4))
				with open("logs/log-{}.json".format(str(dt.date.today())[:7]), 'r') as f:
					t = json.load(f)
					t[str(dt.date.today()-dt.timedelta(days = 1))] = nouveau_jour
					f.close()
				with open("logs/log-{}.json".format(str(dt.date.today())[:7]), 'w') as f:
					f.write(json.dumps(t, indent=4))
				self.day = dt.date.today()

			hourCount()
			self.hour = dt.datetime.now().hour

	@commands.command(pass_context=True)
	async def totalMsg(self, ctx):
		"""
		Permet de savoir combien i y'a eu de message posté depuis que le bot est sur le serveur
		"""
		msg = "Depuis que je suis sur ce serveur il y'a eu : "+str(countTotalMsg())+" messages."
		await ctx.channel.send(msg)

	@commands.command(pass_context=True)
	async def msgBy(self, ctx, Nom=None):
		if len(Nom) == 21 :
			ID = int(Nom[2:20])
		elif len(Nom) == 22 :
			ID = int(Nom[3:21])
		else :
			msg="Le nom que vous m'avez donné n'existe pas !"
			ID = -1

		if (ID != -1):
			res = DB.valueAt(ID, "nbMsg")
			msg=str(Nom)+" a posté "+ str(res) +" messages depuis le "+str(DB.valueAt(ID, "arrival")[:10])
		await ctx.channel.send(msg)

	@commands.command(pass_context=True)
	async def hourMsg(self, ctx, ha=None, hb=None):
		"""
		Permet de savoir combien i y'a eu de message posté dans l'heure ou entre deux heures.
		"""
		d=dt.datetime.now().hour
		if fileExist()==False:
			nbMsg = totalMsg()
			await ctx.channel.send("le fichier time.json est introuvable le résultat sera donc peut être faux.")
		else:
			hourCount()
			with open(file, "r") as f:
				t = json.load(f)
			if ha != None and hb !=None:
				ha=int(ha)
				hb=int(hb)
				if ha >= 0 and hb >= 0 and ha < 24 and hb < 24:
					nbMsg = t[str(hb)]-t[str(ha)]
					msg="Entre "+str(ha)+"h et "+str(hb)+"h il y a eu "+str(nbMsg)+" messages."
				else :
					msg="Vous avez entré une heure impossible."
			else :
				if d != 0:
					nbMsg = t[str(d)]-t[str(d-1)]
				else:
					nbMsg = t["0"]-t["23"]
				msg = "Depuis "+str(d)+"h il y'a eu: "+str(nbMsg)+" messages postés."
		await ctx.channel.send(msg)

	@commands.command(pass_context=True)
	async def graphheure(self, ctx, statue = "local", jour = "now"):
		"""|local/total aaaa-mm-jj| affiche le graph des messages envoyés par heure"""
		if jour =="now":
			jour = str(dt.date.today())
		try :
			logs = json.load(open("logs/log-{}.json".format(jour[:7]),"r"))
		except ValueError :
			ctx.send("la date n'est pas correcte !")
			pass
		log = logs[jour]
		heures = log["msg {} heures".format(statue)]
		if os.path.isfile("cache/graphheure.png"):
			os.remove('cache/graphheure.png')
			print('removed old graphe file')
		x = []
		y = []
		for i in range(24):
			x.append(i)
			y.append(heures[str(i)])
		if statue == "local":
			plt.hist(x, bins = 24, weights = y)
		else :
			plt.plot(x,y,label="graph test")
			plt.fill_between(x, y[0]-100, y, color='blue', alpha=0.5)
		plt.xlabel('heures')
		plt.ylabel('messages')
		plt.title("msg / heure ({})".format(statue))
		plt.savefig("cache/graphheure.png")
		await ctx.send(file=discord.File("cache/graphheure.png"))
		plt.clf()

	@commands.command(pass_context=True)
	async def graphjour(self, ctx, statue = "local", mois = "now"):
		"""|local/total aaaa-mm| affiche le graph des messages envoyés par jour"""
		if mois =="now":
			mois = str(dt.date.today())[:7]
		try :
			logs = json.load(open("logs/log-{}.json".format(mois),"r"))
		except ValueError :
			ctx.send("la date n'est pas correcte !")
			pass
		if os.path.isfile("cache/graphjour.png"):
			os.remove('cache/graphjour.png')
			print('removed old graphe file')
		msg = []
		jour = []
		text = "msg {} jour".format(statue)
		for i in range (1,len(logs)+1):
			if i<10:
				msg.append(logs["{}-0{}".format(mois,i)][text])
			else:
				msg.append(logs["{}-{}".format(mois,i)][text])
			jour.append(i)
		if statue == "local":
			plt.hist(jour, bins = len((logs)), weights = msg)
		else :
			plt.plot(jour,msg,label="graph test")
			plt.fill_between(jour, msg[0]-200, msg, color='blue', alpha=0.5)
		plt.xlabel('jour')
		plt.ylabel('messages')
		plt.title("msg / jour ({})".format(statue))
		plt.savefig("cache/graphjour.png")
		await ctx.send(file=discord.File("cache/graphjour.png"))
		plt.clf()

	@commands.command(pass_context=True)
	async def graphmembre(self, ctx):
		if os.path.isfile("cache/piegraph.png"):
			os.remove('cache/piegraph.png')
			print('removed old graphe file')
		total = countTotalMsg()
		a = []
		for item in DB.db:
			a.append([item["nbMsg"],item["ID"]])
		a.sort(reverse = True)
		richest = a[:6]
		sous_total = 0
		for i in range (6):
			sous_total += richest[i][0]
		labels = []
		sizes = []
		for i in range (6):
			labels.append(ctx.guild.get_member(richest[i][1]).name)
			sizes.append(richest[i][0])
		labels.append("autre")
		sizes.append(total - sous_total)
		explode = (0,0,0,0,0,0,0.2)
		plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90,explode=explode)
		plt.axis('equal')
		plt.savefig('cache/piegraph.png')
		await ctx.send(file=discord.File("cache/piegraph.png"))




def setup(bot):
	bot.add_cog(Stats(bot))
	open("fichier_txt/cogs.txt","a").write("Stats\n")
