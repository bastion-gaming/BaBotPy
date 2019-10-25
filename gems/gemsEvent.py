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
	async def cooking(self, ctx):
		"""**Halloween** | Cuisinons compagnons !!"""
		ID = ctx.author.id
		jour = dt.date.today()
		item = ""
		gain = ""
		maxcooking = 10

		if DB.spam(ID,GF.couldown_4s, "cooked", GF.dbGems):
			if (jour.month == 10 and jour.day >= 26) or (jour.month == 11 and jour.day <= 10):
				item = "pumpkin"
				gain = "pumpkinpie"
			elif (jour.month == 10 and jour.day >= 18) or (jour.month == 1 and jour.day <= 5):
				item = "chocolate"
				gain = "cupcake"
			if item != "":
				nbcooking = DB.nbElements(ID, "inventory", "furnace", GF.dbGems) + 1
				if nbcooking >= maxcooking:
					nbcooking = maxcooking
				if DB.nbElements(ID, "cooked", "furnace_1", GF.dbHH) == 0:
					if DB.nbElements(ID, "inventory", item, GF.dbGems) >= 12:
						DB.add(ID, "cooked", "furnace_1", t.time(), GF.dbHH)
						DB.add(ID, "inventory", item, -12, GF.dbGems)
						desc = "Ton plat a été mis au four. Il aura fini de cuire dans :clock2:`2h`"
					else:
						desc = "Tu n'as pas assez de <:gem_{1}:{0}>`{1}` dans ton inventaire! \n\nIl te faut 12 <:gem_{0}:{1}>`{0}` pour faire 1 <:gem_{2}:{3}>`{2}`".format(item, GF.get_idmoji(item), gain, GF.get_idmoji(gain))
						await ctx.channel.send(desc)
						return False
				else:
					CookedTime = DB.nbElements(ID, "cooked", "furnace_1", GF.dbHH)
					InstantTime = t.time()
					time = CookedTime - (InstantTime-GF.couldown_2h)
					if time <= 0:
						DB.add(ID, "inventory", gain, 1, GF.dbGems)
						DB.add(ID, "cooked", "furnace_1", -1*CookedTime, GF.dbHH)
						desc = "Ton plat à fini de cuire, en le sortant du four tu gagne 1 <:gem_{0}:{1}>`{0}`".format(gain, GF.get_idmoji(gain))
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
				msg = "Commande indisponible! Elle reviendra lors d'un prochain événement."
				await ctx.channel.send(msg)
		else:
			msg = "Il faut attendre "+str(GF.couldown_4s)+" secondes entre chaque commande !"
			await ctx.channel.send(msg)



def setup(bot):
	bot.add_cog(GemsEvent(bot))
	open("help/cogs.txt","a").write("GemsEvent\n")
