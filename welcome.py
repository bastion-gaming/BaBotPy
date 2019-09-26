from discord.ext import commands, tasks
from discord.ext.commands import bot
from discord.utils import get
import discord

import datetime as t
from datetime import datetime

import DB
import stats as stat
import roles

client = discord.Client()


idBASTION = 417445502641111051
idchannel_botplay = 533048015758426112
idchannel_nsfw = 425391362737700894
idcategory_admin = 417453424402235407


async def memberjoin(member, channel):
	if member.guild.id == idBASTION:
		channel_regle = client.get_channel(417454223224209408)
		channel_salon = client.get_channel(545204163341058058)
		channel_presentation = client.get_channel(623077212798582808)
		time = t.time()
		id = member.id
		if DB.newPlayer(id) == "Le joueur a été ajouté !":
			await roles.addrole(member, "Nouveau")
			DB.updateField(id, "arrival", str(t.datetime.now()))
			msg = ":black_small_square:Bienvenue {0} sur Bastion!:black_small_square: \n\n\nNous sommes ravis que tu aies rejoint notre communauté ! \nTu es attendu : \n\n:arrow_right: Sur {1} \n:arrow_right: Sur {2} \n:arrow_right: Sur {3}\nAjoute aussi ton parrain avec `!parrain <Nom>`\n\n=====================".format(member.mention, channel_regle.mention, channel_pres.mention, channel_salon.mention)
		else:
			if DB.valueAt(id, "arrival") == "0":
				DB.updateField(id, "arrival", str(t.datetime.now()))
			await roles.addrole(member, "Nouveau")
			msg = "===================== Bon retour parmis nous ! {0} =====================".format(member.mention)
		stat.countCo()
	else:
		msg = "Bienvenue sur {}".format(member.guild.name)
	print("Welcome >> {} a rejoint le serveur {}".format(member.name, member.guild.name))
	await channel.send(msg)


def memberremove(member):
	if member.guild.id == idBASTION:
		stat.countDeco()
		gems = DB.valueAt(ID, "gems")
		BotGems = DB.valueAt(idBaBot, "gems")
		pourcentage = 0.3
		transfert = gems * pourcentage
		DB.updateField(idBaBot, "gems", BotGems + int(transfert))
		DB.updateField(ID, "gems", gems - int(transfert))
		DB.updateField(ID, "lvl", 0)
		DB.updateField(ID, "xp", 0)
	print("Welcome >> {} a quitté le serveur {}".format(member.name, member.guild.name))



class Welcome(commands.Cog):

	def __init__(self,ctx):
		return(None)



def setup(bot):
	bot.add_cog(Welcome(bot))
	open("fichier_txt/cogs.txt","a").write("Welcome\n")
