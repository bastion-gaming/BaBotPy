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
		"""Date des Événements !!"""
		msg = discord.Embed(title = "Evénements",color= 13752280, description = "Date des Evénements !!")
		desc = "26 Octobre :arrow_right: 10 Novembre"
		for one in GF.objetItem:
			if one.type == "halloween":
				desc += "\n<:gem_{0}:{1}>`{0}`".format(one.nom, GF.get_idmoji(one.nom))
		msg.add_field(name="Halloween", value=desc, inline=False)

		desc = "14 Décembre :arrow_right: 5 Janvier"
		for one in GF.objetItem:
			if one.type == "christmas":
				desc += "\n<:gem_{0}:{1}>`{0}`".format(one.nom, GF.get_idmoji(one.nom))
		desc += ":gift:`gift`"
		msg.add_field(name="Noël", value=desc, inline=False)

		desc = "10 Février :arrow_right: 17 Février"
		for one in GF.objetItem:
			if one.type == "saint valentin":
				desc += "\n<:gem_{0}:{1}>`{0}`".format(one.nom, GF.get_idmoji(one.nom))
		desc += ":gift_heart:`gift_heart`"
		msg.add_field(name="Saint Valentin", value=desc, inline=False)

		desc = "7 Juillet :arrow_right: 21 Juillet"
		msg.add_field(name="Fête Nationale", value=desc, inline=False)
		await ctx.channel.send(embed = msg)


	@commands.command(pass_context=True)
	async def cooking(self, ctx, fct = None):
		"""**Événement** Cuisinons compagnons !!"""
		ID = ctx.author.id
		jour = dt.date.today()
		item = ""
		gain = ""
		i = 1
		maxcooking = 10
		itemHalloween = "pumpkin"
		gainHallowwen = "pumpkinpie"
		itemChristmas = "chocolate"
		gainChristmas = "cupcake"

		if sql.spam(ID,GF.couldown_4s, "cooking", "gems"):
			if (jour.month == 10 and jour.day >= 26) or (jour.month == 11 and jour.day <= 10):
				item = "pumpkin"
				nbitem = 12
			elif (jour.month == 12 and jour.day >= 14) or (jour.month == 1 and jour.day <= 5):
				item = "chocolate"
				nbitem = 8
			if fct == None:
				sql.updateComTime(ID, "cooking", "gems")
				if item != "":
					nbcooking = sql.valueAtNumber(ID, "furnace", "inventory") + 1
					if nbcooking >= maxcooking:
						nbcooking = maxcooking
					msg = discord.Embed(title = "La Cuisine",color= 14902529, description = "")
					while i <= nbcooking:
						data = []
						valueCooking = sql.valueAt(ID, i, "cooking")
						if valueCooking != 0:
							valueTime = float(valueCooking[0])
							valueItem = valueCooking[1]
						else:
							valueTime = 0
							valueItem = ""
						cookingItem = sql.valueAtNumber(ID, item, "inventory")
						if valueTime == 0:
							if cookingItem >= nbitem:
								data.append(str(t.time()))
								data.append(item)
								sql.add(ID, i, data, "cooking")
								sql.add(ID, item, -nbitem, "inventory")
								desc = "Ton plat a été mis au four. Il aura fini de cuire dans :clock2:`2h`"
							else:
								desc = "Tu n'as pas assez de <:gem_{0}:{1}>`{0}` dans ton inventaire! \nIl te faut {4} <:gem_{0}:{1}>`{0}` pour faire 1 <:gem_{2}:{3}>`{2}`".format(item, GF.get_idmoji(item), gain, GF.get_idmoji(gain), nbitem)
						else:
							CookedTime = float(valueTime)
							InstantTime = t.time()
							time = CookedTime - (InstantTime-GF.couldown_2h)
							if time <= 0:
								nbgain = r.randint(1,3)
								data = []
								data.append(0)
								data.append("")
								if valueItem == itemHalloween:
									gain = gainHallowwen
								elif valueItem == itemChristmas:
									gain = gainChristmas
								sql.add(ID, gain, nbgain, "inventory")
								sql.updateField(ID, i, data, "cooking")
								desc = "Ton plat à fini de cuire, en le sortant du four tu gagnes {2} <:gem_{0}:{1}>`{0}`".format(gain, GF.get_idmoji(gain), nbgain)
								lvl.addxp(ID, 1, "gems")
								if i > 1:
									nbfurnace = int(sql.valueAtNumber(ID, "furnace", "inventory"))
									if nbfurnace > 0:
										if sql.valueAtNumber(ID, "furnace", "durability") == 0:
											for c in GF.objetOutil:
												if c.nom == "furnace":
													sql.add(ID, "furnace", c.durabilite, "durability")
										sql.add(ID, "furnace", -1, "durability")
										if sql.valueAtNumber(ID, "furnace", "durability") <= 0:
											for c in GF.objetOutil:
												if c.nom == "furnace":
													sql.add(ID, "furnace", c.durabilite, "durability")
											sql.add(ID, "furnace", -1, "inventory")
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
