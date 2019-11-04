import discord
import random as r
import time as t
import datetime as dt
from DB import DB
from gems import gemsFonctions as GF
from core import welcome as wel, level as lvl
from discord.ext import commands
from discord.ext.commands import bot
from discord.utils import get
from operator import itemgetter


async def action(ctx, IDaction, P, type):
	ID = ctx.author.id
	check = ""
	# Vérifie si le joueur est présent dans une session
	# Si OUI, recupère l'ID de la session

	if DB.OwnerSessionExist(ID, GF.dbSession) == True:
		IDSession = DB.OwnerSessionAt(ID, "ID", GF.dbSession)
		check = "owner"
	else:
		if DB.MemberSessionExist(ID, GF.dbSession) == True:
			IDSession = DB.MemberSessionAt(ID, "ID", GF.dbSession)
			check = "member"
		else:
			await ctx.channel.send("Tu ne peux pas utiliser cette commande. Tu n'as pas accepté de défis.")
			return 404
	if DB.valueAt(IDSession, "sync", GF.dbSession) == "OK":
		CapName = "404"
		for c in GF.objetCapability:
			if c.type == type:
				if "{}".format(c.ID) == IDaction:
					Pmax = c.puissancemax
					CapName = c.nom
		checkCap = False
		CapList = DB.valueAt(ID, "capability", GF.dbGems)
		for one in CapList:
			if one == IDaction:
				checkCap = True
		if CapName == "404":
			await ctx.channel.send("Action impossible! {} inconnu".format(type))
			return 404
		elif not checkCap:
			await ctx.channel.send("Tu ne pocèdes pas cette aptitude!")
			return False
		else:
			if int(P) > Pmax:
				P = Pmax
			elif int(P) <= 0:
				P = 0
			if DB.spam(ID,GF.couldown_4s, type, GF.dbGems):
				for c in GF.objetCapability:
					if "{}".format(c.ID) == IDaction:
						ActionItem = c.item
				if DB.nbElements(ID, "inventory", ActionItem, GF.dbGems) >= 1:
					action = []
					action.append(IDaction)
					action.append(P)
					if check == "owner":
						DB.updateField(IDSession, "actionOwner", action, GF.dbSession)
					elif check == "member":
						DB.updateField(IDSession, "actionMember", action, GF.dbSession)
					msg = "_Action de **{}** prise en compte_".format(ctx.author.name)
					DB.updateComTime(ID, type, GF.dbGems)
					await ctx.message.delete(delay=1)
					await ctx.channel.send(msg)
					if checkround(IDSession):
						await ctx.channel.send(embed = round(ctx, IDSession))
						await checklife(ctx, IDSession)
						return True
				else:
					await ctx.message.delete(delay=1)
					msg = "**_{2}_** | Action impossible! Tu n'as pas assez de <:gem_{0}:{1}>`{0}` dans ton inventaire.".format(ActionItem, GF.get_idmoji(ActionItem), ctx.author.name)
					await ctx.channel.send(msg)
			else:
				msg = "Il faut attendre "+str(GF.couldown_4s)+" secondes entre chaque commande !"
				await ctx.channel.send(msg)
			return True
	else:
		await ctx.channel.send("Défis non synchronisé")
		return False


def checkround(IDSession):
	valueOwner = DB.valueAt(IDSession, "actionOwner", GF.dbSession)
	valueMember = DB.valueAt(IDSession, "actionMember", GF.dbSession)
	if valueOwner != [] and valueMember != []:
		return True
	else:
		return False


async def checklife(ctx, IDSession):
	lifeOwner = DB.valueAt(IDSession, "lifeOwner", GF.dbSession)
	lifeMember = DB.valueAt(IDSession, "lifeMember", GF.dbSession)
	member = DB.valueAt(IDSession, "member", GF.dbSession)
	owner = ctx.guild.get_member(DB.valueAt(IDSession, "owner", GF.dbSession))
	mise = DB.valueAt(IDSession, "mise", GF.dbSession)
	if lifeOwner <= 0 and lifeMember <= 0:
		desc = "Fin du duel\n\nMatch nul. Personne ne remprote la victoire!"
		msg = discord.Embed(title = "Defis {}".format(DB.valueAt(IDSession, "ID", GF.dbSession)),color= 13752280, description = desc)
		await ctx.channel.send(embed = msg)
		msg = "••••••••••\n<:gem_sword:{1}> Match Nul! Fin du defis `{0}`".format(IDSession, GF.get_idmoji("sword"))
		DB.removePlayer(IDSession, GF.dbSession)
		await owner.send(msg)
		for userID in member:
			user = ctx.guild.get_member(userID)
			await user.send(msg)
		return "end"
	elif lifeOwner <= 0 or lifeMember <= 0:
		if lifeOwner <= 0:
			for userID in member:
				win = ctx.guild.get_member(userID)
				winID = userID
			lostID = DB.valueAt(IDSession, "owner", GF.dbSession)
		elif lifeMember <= 0:
			win = owner
			winID = DB.valueAt(IDSession, "owner", GF.dbSession)
			for userID in member:
				lostID = userID
		desc = "Duel terminée\nLa victoire revient à {0}\nTu gagne les {1} :gem:`gems` de ton adversaire".format(win.name, mise)
		msg = discord.Embed(title = "Defis {}".format(DB.valueAt(IDSession, "ID", GF.dbSession)),color= 13752280, description = desc)
		await ctx.channel.send(embed = msg)
		DB.addGems(winID, mise)
		lost_nbGems = DB.valueAt(lostID, "gems", GF.dbGems)
		if lost_nbGems < mise:
			DB.addGems(lostID, -lostnbGems)
		else:
			DB.addGems(lostID, -mise)
		msg = "••••••••••\n<:gem_sword:{1}>Fin du defis `{0}`\n<@{1}> a gagné".format(IDSession, GF.get_idmoji("sword"), winID)
		DB.removePlayer(IDSession, GF.dbSession)
		await owner.send(msg)
		for userID in member:
			user = ctx.guild.get_member(userID)
			await user.send(msg)
		return "end"
	else:
		return True


def round(ctx, IDSession):
	valueOwner = DB.valueAt(IDSession, "actionOwner", GF.dbSession)
	OwnerLife = DB.valueAt(IDSession, "lifeOwner", GF.dbSession)
	IDowner = DB.valueAt(IDSession, "owner", GF.dbSession)
	userOwner = ctx.guild.get_member(IDowner)
	OwnerAction = valueOwner[0]
	OwnerPuissance = int(valueOwner[1])

	valueMember = DB.valueAt(IDSession, "actionMember", GF.dbSession)
	MemberLife = DB.valueAt(IDSession, "lifeMember", GF.dbSession)
	member = DB.valueAt(IDSession, "member", GF.dbSession)
	for one in member:
		userMember = ctx.guild.get_member(one)
		IDmember = one
	MemberAction = valueMember[0]
	MemberPuissance = int(valueMember[1])

	OwnerType = ""
	MemberType = ""
	result = ""

	for c in GF.objetCapability:
		if "{}".format(c.ID) == OwnerAction:
			OwnerType = c.type
			OwnerActionName = c.nom
			OwnerItem = c.item
			OwnerNBperte = c.nbperte

		if "{}".format(c.ID) == MemberAction:
			MemberType = c.type
			MemberActionName = c.nom
			MemberItem = c.item
			MemberNBperte = c.nbperte

	OwnerDesc = "Action: _{0}_ | **{1}** \nPuissance: {2}".format(OwnerType, OwnerActionName, OwnerPuissance)
	MemberDesc = "Action: _{0}_ | **{1}** \nPuissance: {2}".format(MemberType, MemberActionName, MemberPuissance)

	# Defense vs Defense
	if OwnerType == "defense" and MemberType == "defense":
		result = "Personne n'as perdu de :hearts:\n"
		result += "**{0}** {1} :hearts:\n".format(userOwner.name, DB.valueAt(IDSession, "lifeOwner", GF.dbSession))
		result += "**{0}** {1} :hearts:\n".format(userMember.name, DB.valueAt(IDSession, "lifeMember", GF.dbSession))

	# Attaque vs Attaque
	elif OwnerType == "attaque" and MemberType == "attaque":
		OwnerDurabilite = GF.get_durabilite(userOwner.id, OwnerItem)
		if OwnerDurabilite == None:
			OwnerDesc += "\n**-{2}** de durabilité pour ta <:gem_{0}:{1}>`{0}`".format(OwnerItem, GF.get_idmoji(OwnerItem), OwnerPuissance)
			for c in GF.objetOutil:
				if c.nom == OwnerItem:
					GF.addDurabilite(userOwner.id, c.nom, c.durabilite)
			GF.addDurabilite(userOwner.id, OwnerItem, -OwnerPuissance)
		elif int(OwnerDurabilite) > OwnerPuissance:
			OwnerDesc += "\n**-{2}** de durabilité pour ta <:gem_{0}:{1}>`{0}`".format(OwnerItem, GF.get_idmoji(OwnerItem), OwnerPuissance)
			GF.addDurabilite(userOwner.id, OwnerItem, -OwnerPuissance)
		else:
			OwnerDurabilite = int(OwnerDurabilite)
			OwnerDesc += "\n:cry: Pas de chance tu as cassé ta <:gem_{0}:{1}>`{0}` !".format(OwnerItem, GF.get_idmoji(OwnerItem))
			temp = OwnerPuissance - OwnerDurabilite
			DB.add(userOwner.id, "inventory", OwnerItem, -1, GF.dbGems)
			if DB.nbElements(userOwner.id, "inventory", OwnerItem, GF.dbGems) > 0:
				for c in GF.objetOutil:
					if c.nom == OwnerItem:
						GF.addDurabilite(userOwner.id, c.nom, c.durabilite-OwnerDurabilite-temp)

		MemberDurabilite = GF.get_durabilite(userMember.id, MemberItem)
		if MemberDurabilite == None:
			MemberDesc += "\n**-{2}** de durabilité pour ta <:gem_{0}:{1}>`{0}`".format(MemberItem, GF.get_idmoji(MemberItem), MemberPuissance)
			for c in GF.objetOutil:
				if c.nom == MemberItem:
					GF.addDurabilite(userMember.id, c.nom, c.durabilite)
			GF.addDurabilite(userMember.id, MemberItem, -MemberPuissance)
		elif MemberDurabilite > MemberPuissance:
			MemberDesc += "\n**-{2}** de durabilité pour ta <:gem_{0}:{1}>`{0}`".format(MemberItem, GF.get_idmoji(MemberItem), MemberPuissance)
			GF.addDurabilite(userMember.id, MemberItem, -MemberPuissance)
		else:
			MemberDesc += "\n:cry: Pas de chance tu as cassé ta <:gem_{0}:{1}>`{0}` !".format(MemberItem, GF.get_idmoji(MemberItem))
			temp = MemberPuissance - MemberDurabilite
			DB.add(userMember.id, "inventory", MemberItem, -1, GF.dbGems)
			if DB.nbElements(userMember.id, "inventory", MemberItem, GF.dbGems) > 0:
				for c in GF.objetOutil:
					if c.nom == MemberItem:
						GF.addDurabilite(userMember.id, c.nom, c.durabilite-MemberDurabilite-temp)

		DB.updateField(IDSession, "lifeOwner", OwnerLife-MemberPuissance, GF.dbSession)
		DB.updateField(IDSession, "lifeMember", MemberLife-OwnerPuissance, GF.dbSession)

		result = "**{0}** {1} :hearts:\n".format(userOwner.name, DB.valueAt(IDSession, "lifeOwner", GF.dbSession))
		result += "**{0}** {1} :hearts:\n".format(userMember.name, DB.valueAt(IDSession, "lifeMember", GF.dbSession))

	# Defense vs Attaque
	elif OwnerType == "defense" and MemberType == "attaque":
		DB.add(userOwner.id, "inventory", OwnerItem, -OwnerPuissance*OwnerNBperte, GF.dbGems)
		OwnerDesc += "\n**{0}** a perdu {3}<:gem_{1}:{2}>`{1}`\n".format(userOwner.name, OwnerItem, GF.get_idmoji(OwnerItem), OwnerPuissance)

		MemberDurabilite = GF.get_durabilite(userMember.id, MemberItem)
		if MemberDurabilite == None:
			MemberDesc += "\n**-{2}** de durabilité pour ta <:gem_{0}:{1}>`{0}`".format(MemberItem, GF.get_idmoji(MemberItem), MemberPuissance)
			for c in GF.objetOutil:
				if c.nom == MemberItem:
					GF.addDurabilite(userMember.id, c.nom, c.durabilite)
			GF.addDurabilite(userMember.id, MemberItem, -MemberPuissance)
		elif MemberDurabilite > MemberPuissance:
			MemberDesc += "\n**-{2}** de durabilité pour ta <:gem_{0}:{1}>`{0}`".format(MemberItem, GF.get_idmoji(MemberItem), MemberPuissance)
			GF.addDurabilite(userMember.id, MemberItem, -MemberPuissance)
		else:
			MemberDurabilite = int(MemberDurabilite)
			MemberDesc += "\n:cry: Pas de chance tu as cassé ta <:gem_{0}:{1}>`{0}` !".format(MemberItem, GF.get_idmoji(MemberItem))
			temp = MemberPuissance - MemberDurabilite
			DB.add(userMember.id, "inventory", MemberItem, -1, GF.dbGems)
			if DB.nbElements(userMember.id, "inventory", MemberItem, GF.dbGems) > 0:
				for c in GF.objetOutil:
					if c.nom == MemberItem:
						GF.addDurabilite(userMember.id, c.nom, c.durabilite-MemberDurabilite-temp)
		temp = MemberPuissance - OwnerPuissance
		if temp > 0:
			DB.updateField(IDSession, "lifeOwner", OwnerLife-temp, GF.dbSession)
		elif temp < 0:
			temp = -temp
			DB.updateField(IDSession, "lifeMember", OwnerMember-temp, GF.dbSession)
			result = "Effet miroir!\nLa défense est plus puissante que l'attaque et renvoie la différence à l'attaquant."

		result += "**{0}** {1} :hearts:\n".format(userOwner.name, DB.valueAt(IDSession, "lifeOwner", GF.dbSession))
		result += "**{0}** {1} :hearts:\n".format(userMember.name, DB.valueAt(IDSession, "lifeMember", GF.dbSession))

	# Attaque vs Defense
	elif OwnerType == "attaque" and MemberType == "defense":
		DB.add(userMember.id, "inventory", MemberItem, -MemberPuissance*MemberNBperte, GF.dbGems)
		MemberDesc += "\n**{0}** a perdu {3}<:gem_{1}:{2}>`{1}`\n".format(userMember.name, MemberItem, GF.get_idmoji(MemberItem), MemberPuissance)

		OwnerDurabilite = GF.get_durabilite(userOwner.id, OwnerItem)
		if OwnerDurabilite == None:
			OwnerDesc += "\n**-{2}** de durabilité pour ta <:gem_{0}:{1}>`{0}`".format(OwnerItem, GF.get_idmoji(OwnerItem), OwnerPuissance)
			for c in GF.objetOutil:
				if c.nom == OwnerItem:
					GF.addDurabilite(userOwner.id, c.nom, c.durabilite)
			GF.addDurabilite(userOwner.id, OwnerItem, -OwnerPuissance)
		if OwnerDurabilite > OwnerPuissance:
			OwnerDesc += "\n**-{2}** de durabilité pour ta <:gem_{0}:{1}>`{0}`".format(OwnerItem, GF.get_idmoji(OwnerItem), OwnerPuissance)
			GF.addDurabilite(userOwner.id, OwnerItem, -OwnerPuissance)
		else:
			OwnerDurabilite = int(OwnerDurabilite)
			OwnerDesc += "\n:cry: Pas de chance tu as cassé ta <:gem_{0}:{1}>`{0}` !".format(OwnerItem, GF.get_idmoji(OwnerItem))
			temp = OwnerPuissance - OwnerDurabilite
			DB.add(userOwner.id, "inventory", OwnerItem, -1, GF.dbGems)
			if DB.nbElements(userOwner.id, "inventory", OwnerItem, GF.dbGems) > 0:
				for c in GF.objetOutil:
					if c.nom == OwnerItem:
						GF.addDurabilite(userOwner.id, c.nom, c.durabilite-OwnerDurabilite-temp)

		temp = OwnerPuissance - MemberPuissance
		if temp > 0:
			DB.updateField(IDSession, "lifeMember", MemberLife-temp, GF.dbSession)
		elif temp < 0:
			temp = -temp
			DB.updateField(IDSession, "lifeOwner", OwnerLife-temp, GF.dbSession)
			result = "Effet miroir!\nLa défense est plus puissante que l'attaque et renvoie la différence à l'attaquant."

		result += "**{0}** {1} :hearts:\n".format(userOwner.name, DB.valueAt(IDSession, "lifeOwner", GF.dbSession))
		result += "**{0}** {1} :hearts:\n".format(userMember.name, DB.valueAt(IDSession, "lifeMember", GF.dbSession))

	nbRound = DB.valueAt(IDSession, "round", GF.dbSession)
	msg = discord.Embed(title = "Round {}".format(nbRound),color= 13752280, description = "")
	msg.add_field(name="{}".format(userOwner.name), value=OwnerDesc, inline=False)
	msg.add_field(name="{}".format(userMember.name), value=MemberDesc, inline=False)
	msg.add_field(name="Résultats", value=result, inline=False)

	DB.updateField(IDSession, "actionOwner", [], GF.dbSession)
	DB.updateField(IDSession, "actionMember", [], GF.dbSession)
	DB.updateField(IDSession, "round", nbRound+1, GF.dbSession)
	lvl.addxp(IDowner, 10, GF.dbGems)
	lvl.addxp(IDmember, 10, GF.dbGems)
	return msg


class GemsFight(commands.Cog):

	def __init__(self,ctx):
		return(None)



	@commands.command(pass_context=True)
	async def defis(self, ctx, opt, arg1, mise = None):
		"""
		**duel [nom] [mise]** | Gestion des sessions de duel
		"""
		ID = ctx.author.id
		IDmember = DB.nom_ID(arg1)
		if opt == "duel":
			if ID == IDmember:
				await ctx.channel.send("Tu ne peux pas te défier toi même")
				return False
			elif mise != None:
				imise = int(mise)
			else:
				await ctx.channel.send("Il manque la mise pour lancer ce défis")
				return False
			if DB.valueAt(ID, "gems", GF.dbGems) >= imise and DB.valueAt(IDmember, "gems", GF.dbGems) >= imise:
				# arg1 >> utilisateur à défier
				if DB.OwnerSessionExist(ID, GF.dbSession) == False:
					if DB.MemberSessionExist(IDmember, GF.dbSession) == False or DB.MemberSessionExist(ID, GF.dbSession) == False:
						check = True
						while check:
							try:
								code = GF.gen_code()
								DB.valueAt(code, "ID", GF.dbSession)
							except:
								check = False
						if DB.newPlayer(code, GF.dbSession, GF.dbSessionTemplate) == "Le joueur a été ajouté !":
							DB.updateField(code, "owner", ID, GF.dbSession)
							DB.updateField(code, "type", "duel", GF.dbSession)
							DB.updateField(code, "mise", imise, GF.dbSession)
							DB.updateField(code, "sync", "NOK", GF.dbSession)
							member = DB.valueAt(code, "member", GF.dbSession)
							member.append(IDmember)
							DB.updateField(code, "member", member, GF.dbSession)
							msg = "Défis `{}` créée".format(code)
							user = ctx.guild.get_member(IDmember)
							msg += "\n Message envoyer à {}\n••••\nEn attende de synchronisation".format(user.name)
							mpuser = "••••••••••\n<:gem_sword:{2}> {0} ta défié en duel <:gem_sword:{2}>\nMise: {3} :gem:`gems`\n\n2 choix s'offre à toi:\n- Tu peux accepter le defis en utilisant la commande `!defis accept {1}`\n- Tu peux refuser le defis en utilisant la commande `!defis deny {1}`\n\nBalance de {5}: {4} :gem:`gems`".format(ctx.author.name, code, GF.get_idmoji("sword"), imise, DB.valueAt(IDmember, "gems", GF.dbGems), ctx.guild.get_member(IDmember).name)
							try:
								await user.send(mpuser)
								await ctx.channel.send(msg)
							except:
								DB.removePlayer(code, GF.dbSession)
								await ctx.channel.send("Défis impossible! tu ne peux pas défier un bot")
					else:
						await ctx.channel.send("Ce joueur à déjà été défié!")
				else:
					await ctx.channel.send("Tu as déjà créé une session de duel. Pour y mettre fin et en créé une nouvelle utilise la commande `!defis end {0}`".format(DB.OwnerSessionAt(ctx.author.id, "ID", GF.dbSession)))
			else:
				await ctx.channel.send("Défis impossible! **{0}** ou **{1}** n'as pas assez de :gem:`gems` en banque.".format(ctx.guild.get_member(IDmember).name, ctx.author.name))
		elif opt == "end":
			# arg1 >> code d'identification de la session
			try:
				if DB.valueAt(arg1, "type", GF.dbSession) == "duel":
					member = DB.valueAt(arg1, "member", GF.dbSession)
					check = False
					for one in member:
						if one == ctx.author.id:
							check = True
					if DB.valueAt(arg1, "owner", GF.dbSession) == ctx.author.id or check:
						await ctx.channel.send("{1} a mis fin au defis `{0}`".format(arg1, ctx.author.name))
						msg = "••••••••••\n<:gem_sword:{2}> {1} a mis fin au defis `{0}`".format(arg1, ctx.author.name, GF.get_idmoji("sword"))
						owner = ctx.guild.get_member(DB.valueAt(arg1, "owner", GF.dbSession))
						DB.removePlayer(arg1, GF.dbSession)
						await owner.send(msg)
						for userID in member:
							user = ctx.guild.get_member(userID)
							await user.send(msg)
					else:
						await ctx.channel.send("Tu n'as pas les autorisations pour mettre fin au défis `{}`".format(arg1))
				else:
					await ctx.channel.send("Code défis inconnu")
			except:
				await ctx.channel.send("Code défis inconnu")
		elif opt == "deny":
			# arg1 >> code d'identification de la session
			try:
				if DB.valueAt(arg1, "type", GF.dbSession) == "duel":
					member = DB.valueAt(arg1, "member", GF.dbSession)
					check = False
					for one in member:
						if one == ctx.author.id:
							check = True
					if check:
						DB.removePlayer(arg1, GF.dbSession)
						await ctx.channel.send("{1} a refusé le defis `{0}`".format(arg1, ctx.author.name))
						owner = ctx.guild.get_member(DB.valueAt(arg1, "owner", GF.dbSession))
						await owner.send("<:gem_sword:{2}> {1} a refusé votre défis `{0}`".format(arg1, ctx.author.mention, GF.get_idmoji("sword")))
					elif DB.valueAt(arg1, "owner", GF.dbSession) == ctx.author.id:
						await ctx.channel.send("Tu ne peux pas refusé ton propre défis.\nSi tu veux mettre fin au défis utilise la commande `!defis end {}`".format(arg1))
					else:
						await ctx.channel.send("Tu n'as pas les autorisations pour refusé le défis `{}`".format(arg1))
				else:
					await ctx.channel.send("Code défis inconnu")
			except:
				await ctx.channel.send("Code défis inconnu")
		elif opt == "accept":
			# arg1 >> code d'identification de la session
			try:
				if DB.valueAt(arg1, "type", GF.dbSession) == "duel":
					member = DB.valueAt(arg1, "member", GF.dbSession)
					check = False
					for one in member:
						if one == ctx.author.id:
							userMember = ctx.guild.get_member(one)
							check = True
					if check:
						DB.updateField(arg1, "sync", "OK", GF.dbSession)
						msg = "••••••••••\n<:gem_sword:{2}> {1} a accepté le defis `{0}`".format(arg1, ctx.author.name, GF.get_idmoji("sword"))
						owner = ctx.guild.get_member(DB.valueAt(arg1, "owner", GF.dbSession))
						await owner.send(msg)
						msg = "__Commandes utiles__:"
						msg += "\n`!inv capabilities` :arrow_forward: Permet de voir la liste de tes Attaque/Défense.\n"
						msg += "\n`!attack [ID de l'attaque] [Puissance]` :arrow_forward: Permet de lancer une attaque pour reduire la vie de l'adversaire."
						msg += "\n`!defense [ID de la defense] [Puissance]` :arrow_forward: Permet de lancer une defense pour contré l'attaque d'un adversaire."
						msg += "\n_Si la puissance n'est pas indiquée alors elle sera aléatoire_"
						msg += "\n\n`!defis end {}` :arrow_forward: Mettre fin au défis".format(arg1)
						await owner.send(msg)
						await userMember.send(msg)
						msg = "{1} a accepté le defis de {0}".format(owner.name, ctx.author.name)
						await ctx.channel.send(msg)
				else:
					await ctx.channel.send("Code défis inconnu")
			except:
				await ctx.channel.send("Code défis inconnu")


	@commands.command(pass_context=True)
	async def attack(self, ctx, IDatt, P = None):
		"""
		**[ID] [Puissance]** | Lance l'attaque correspondant à l'ID avec la puissance spécifiée
		"""
		if P == None:
			P = r.randint(1,10)
		await action(ctx, IDatt, P, "attaque")


	@commands.command(pass_context=True)
	async def defense(self, ctx, IDatt, P = None):
		"""
		**[ID] [Puissance]** | Lance la defense correspondant à l'ID avec la puissance spécifiée
		"""
		if P == None:
			P = r.randint(1,10)
		await action(ctx, IDatt, P, "defense")




def setup(bot):
	bot.add_cog(GemsFight(bot))
	open("help/cogs.txt","a").write("GemsFight\n")
