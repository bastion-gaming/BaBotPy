import discord
import random as r
import time as t
import datetime as dt
from DB import TinyDB as DB, SQLite as sql
from gems import gemsFonctions as GF
from core import level as lvl
from discord.ext import commands
from discord.ext.commands import bot
from discord.utils import get
from operator import itemgetter

class GemsEvent(commands.Cog):

	def __init__(self,ctx):
		return(None)


	@commands.command(pass_context=True)
	async def event(self, ctx):
		"""Date des Evénements !!"""
		msg = discord.Embed(title = "Evénements",color= 13752280, description = "Date des Evénements !!")
		desc = "26 Octobre :arrow_right: 10 Novembre"
		msg.add_field(name="Halloween", value=desc, inline=False)
		desc = "14 Décembre :arrow_right: 5 Janvier"
		msg.add_field(name="Noël", value=desc, inline=False)
		await ctx.channel.send(embed = msg)


	@commands.command(pass_context=True)
	async def cooking(self, ctx, fct = None):
		"""**Evénement** Cuisinons compagnons !!"""
		ID = ctx.author.id
		jour = dt.date.today()
		item = ""
		gain = ""
		i = 1
		maxcooking = 10

		if DB.spam(ID,GF.couldown_4s, "cooked", GF.dbGems):
			if (jour.month == 10 and jour.day >= 26) or (jour.month == 11 and jour.day <= 10):
				item = "pumpkin"
				gain = "pumpkinpie"
				nbitem = 12
			elif (jour.month == 10 and jour.day >= 14) or (jour.month == 1 and jour.day <= 5):
				item = "chocolate"
				gain = "cupcake"
				nbitem = 8
			if fct == None:
				DB.updateComTime(ID, "cooked", GF.dbGems)
				if item != "":
					nbcooking = DB.nbElements(ID, "inventory", "furnace", GF.dbGems) + 1
					if nbcooking >= maxcooking:
						nbcooking = maxcooking
					msg = discord.Embed(title = "La Cuisine",color= 14902529, description = "")
					while i <= nbcooking:
						if DB.nbElements(ID, "cooked", "furnace_{}".format(i), GF.dbHH) == 0:
							if DB.nbElements(ID, "inventory", item, GF.dbGems) >= nbitem:
								DB.add(ID, "cooked", "furnace_{}".format(i), t.time(), GF.dbHH)
								DB.add(ID, "inventory", item, -nbitem, GF.dbGems)
								desc = "Ton plat a été mis au four. Il aura fini de cuire dans :clock2:`2h`"
							else:
								desc = "Tu n'as pas assez de <:gem_{0}:{1}>`{0}` dans ton inventaire! \nIl te faut {4} <:gem_{0}:{1}>`{0}` pour faire 1 <:gem_{2}:{3}>`{2}`".format(item, GF.get_idmoji(item), gain, GF.get_idmoji(gain), nbitem)
						else:
							CookedTime = DB.nbElements(ID, "cooked", "furnace_{}".format(i), GF.dbHH)
							InstantTime = t.time()
							time = CookedTime - (InstantTime-GF.couldown_2h)
							if time <= 0:
								nbgain = r.randint(1,3)
								DB.add(ID, "inventory", gain, nbgain, GF.dbGems)
								DB.add(ID, "cooked", "furnace_{}".format(i), -1*CookedTime, GF.dbHH)
								desc = "Ton plat à fini de cuire, en le sortant du four tu gagne {2} <:gem_{0}:{1}>`{0}`".format(gain, GF.get_idmoji(gain), nbgain)
								lvl.addxp(ID, 1, GF.dbGems)
								if i > 1:
									if DB.nbElements(ID, "inventory", "furnace", GF.dbGems) > 0:
										if GF.get_durabilite(ID, "furnace") == None:
											for c in GF.objetOutil:
												if c.nom == "furnace":
													GF.addDurabilite(ID, c.nom, c.durabilite)
										GF.addDurabilite(ID, "furnace", -1)
										if GF.get_durabilite(ID, "furnace") <= 0:
											for c in GF.objetOutil:
												if c.nom == "furnace":
													GF.addDurabilite(ID, c.nom, c.durabilite)
											DB.add(ID, "inventory", "furnace", -1, GF.dbGems)
							else:
								timeH = int(time / 60 / 60)
								time = time - timeH * 3600
								timeM = int(time / 60)
								timeS = int(time - timeM * 60)
								desc = "Ton plat aura fini de cuir dans :clock2:`{}h {}m {}s`".format(timeH,timeM,timeS)
						msg.add_field(name="Four n°{}".format(i), value=desc, inline=False)
						i += 1
					await ctx.channel.send(embed = msg)
				else:
					msg = "Commande indisponible! Elle reviendra lors d'un prochain événement."
					await ctx.channel.send(msg)
			else:
				msg = "Fonction inconnu"
				await ctx.channel.send(msg)
				return False
		else:
			msg = "Il faut attendre "+str(GF.couldown_4s)+" secondes entre chaque commande !"
			await ctx.channel.send(msg)



def setup(bot):
	bot.add_cog(GemsEvent(bot))
	open("help/cogs.txt","a").write("GemsEvent\n")
