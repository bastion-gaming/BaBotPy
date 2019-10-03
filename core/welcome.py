from discord.ext import commands, tasks
from discord.ext.commands import bot
from discord.utils import get
import discord

import datetime as t
from datetime import datetime

from DB import DB
from core import roles, stats as stat

client = discord.Client()

idBaBot = 604776153458278415
idGetGems = 620558080551157770

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
			msg = ":black_small_square:Bienvenue {0} sur Bastion!:black_small_square: \n\n\nNous sommes ravis que tu aies rejoint notre communauté ! \nTu es attendu : \n\n:arrow_right: Sur `# règles`\n:arrow_right: Sur `# présentation` \n:arrow_right: Sur `# liste-salon`\nAjoute aussi ton parrain avec `!parrain <Nom>`\n\n=====================".format(member.mention)
		else:
			if DB.valueAt(id, "arrival") == "0":
				DB.updateField(id, "arrival", str(t.datetime.now()))
			await roles.addrole(member, "Nouveau")
			msg = "===================== Bon retour parmis nous ! {0} =====================".format(member.mention)
		stat.countCo()
	else:
		msg = "Bienvenue {} sur {}".format(member.mention, member.guild.name)
	print("Welcome >> {} a rejoint le serveur {}".format(member.name, member.guild.name))
	await channel.send(msg)


def memberremove(member):
	ID = member.id
	gems = DB.valueAt(ID, "gems")
	if member.guild.id == idBASTION:
		stat.countDeco()
		BotGems = DB.valueAt(idBaBot, "gems")
		idBot = idBaBot
		pourcentage = 0.3
		DB.updateField(ID, "lvl", 0)
		DB.updateField(ID, "xp", 0)
	else:
		BotGems = DB.valueAt(idGetGems, "gems")
		idBot = idGetGems
		pourcentage = 0.02
	transfert = gems * pourcentage
	DB.updateField(idBot, "gems", BotGems + int(transfert))
	DB.updateField(ID, "gems", gems - int(transfert))
	# DB.removePlayer(member.id)
	print("Welcome >> {} a quitté le serveur {}".format(member.name, member.guild.name))



class Welcome(commands.Cog):

	def __init__(self,ctx):
		return(None)



def setup(bot):
	bot.add_cog(Welcome(bot))
	open("help/cogs.txt","a").write("Welcome\n")
