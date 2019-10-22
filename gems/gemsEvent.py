import discord
import random as r
import time as t
import datetime as dt
from DB import DB
from gems import gemsFonctions as GF
from discord.ext import commands
from discord.ext.commands import bot
from discord.utils import get
from operator import itemgetter

class GemsEvent(commands.Cog):

	def __init__(self,ctx):
		return(None)



	@commands.command(pass_context=True)
	async def cooked(self, ctx):
		"""**Halloween** | Cuisinons compagnons !!"""
		ID = ctx.author.id
		if DB.spam(ID,GF.couldown_l, "cooked", GF.dbGems):
			if DB.nbElements(ID, "cooked", "furnace_1", GF.dbGems) == 0:
				if DB.nbElements(ID, "inventory", "pumpkin", GF.dbGems) >= 12:
					DB.add(ID, "cooked", "furnace_1", t.time(), GF.dbGems)
					DB.add(ID, "inventory", "pumpkin", -12, GF.dbGems)
					desc = "Votre plat a été mis au four".format(GF.get_idmoji("seed"))
				else:
					desc = "Tu n'as pas assez de <:gem_pumpkin:{0}>`pumpkin` dans ton inventaire! \n\nIl te faut 12 <:gem_pumpkin:{0}>`pumpkin` pour faire une <:gem_pumpkinpie:{1}>`pumpkinpie`".format(GF.get_idmoji("pumpkin"), GF.get_idmoji("pumpkinpie"))
					await ctx.channel.send(desc)
					return False
			else:
				CookedTime = DB.nbElements(ID, "cooked", "furnace_1", GF.dbGems)
				InstantTime = t.time()
				time = CookedTime - (InstantTime-GF.couldown_2h)
				if time <= 0:
					DB.add(ID, "inventory", "oak", 1, GF.dbGems)
					DB.add(ID, "cooked", "furnace_1", -1*CookedTime, GF.dbGems)
					desc = "Ton plat à fini de cuir, en le sortant du four tu gagne 1 <:gem_pumpkinpie:{}>`pumpkinpie`".format(GF.get_idmoji("pumpkinpie"))
					D = r.randint(0,20)
					if D == 20 or D == 0:
						DB.add(ID, "inventory", "lootbox_raregems", 1, GF.dbGems)
						desc += "\nTu as trouvé une **Loot Box Gems Rare**! Utilise la commande `boxes open raregems` pour l'ouvrir"
					elif D >= 9 and D <= 11:
						DB.add(ID, "inventory", "lootbox_commongems", 1, GF.dbGems)
						desc += "\nTu as trouvé une **Loot Box Gems Common**! Utilise la commande `boxes open commongems` pour l'ouvrir"
				else:
					timeH = int(time / 60 / 60)
					time = time - timeH * 3600
					timeM = int(time / 60)
					timeS = int(time - timeM * 60)
					desc = "Ton plat aura fini de cuir dans :clock2:`{}h {}m {}s`".format(timeH,timeM,timeS)
			msg = discord.Embed(title = "La Cuisine",color= 14902529, description = desc)
			await ctx.channel.send(embed = msg)
			DB.updateComTime(ID, "cooked", GF.dbGems)
		else:
			msg = "Il faut attendre "+str(GF.couldown_l)+" secondes entre chaque commande !"
			await ctx.channel.send(msg)



def setup(bot):
	bot.add_cog(GemsEvent(bot))
	open("help/cogs.txt","a").write("GemsEvent\n")
