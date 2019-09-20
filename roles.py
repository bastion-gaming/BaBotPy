import discord
from discord.ext import commands
from discord.ext.commands import bot
from discord.utils import get
import gestion as ge
import DB

rolelist = ["BastioBot","Ingénieur du Bastion","Responsable Twitch","PEGI master","Pollmaster","Groovy","Bastion RPG","Ambassadeur","Candidat Ambassade","Twitcher","Joueurs"]

async def addrole(member, role):
	setrole = get(member.guild.roles, name=role)
	await member.add_roles(setrole)

class Roles(commands.Cog):

	def __init__(self,ctx):
		return(None)

	@commands.command(pass_context=True)
	async def gamecreate(self, ctx, game, categorie = None):
		"""**[jeu] [grand salon]** | Permet de créer un nouveau role pour un jeu et d'ajouter ce jeu dans un grand salon"""
		# Paramètres:
		# - game: Nom du jeu/role
		# - categorie: Nom du grand salon (combat/societe/tirs/voiture/rpg/sandbox/strategie/divers)
		guild = ctx.guild
		member = ctx.author
		rolesearch = discord.utils.get(member.guild.roles, name=game)
		if ge.permission(ctx, ge.Ambassadeur)==True:
			if rolesearch == None:
				await guild.create_role(name=game)
				desc = "Le jeu '"+game+"' a été créé"

				if categorie != None:
					rolesearch = discord.utils.get(member.guild.roles, name=game)
					categorie = categorie.lower()

					if categorie == "combat":
						channeladd = guild.get_channel(589944955800256515)
					elif categorie == "societe":
						channeladd = guild.get_channel(589945591203889152)
					elif categorie == "tirs":
						channeladd = guild.get_channel(589946246437797888)
					elif categorie == "voiture":
						channeladd = guild.get_channel(589946276540448821)
					elif categorie == "rpg":
						channeladd = guild.get_channel(589946305917222916)
					elif categorie == "sandbox":
						channeladd = guild.get_channel(589946380416581632)
					elif categorie == "strategie":
						channeladd = guild.get_channel(589953946639007764)
					elif categorie == "divers":
						channeladd = guild.get_channel(590664052318142474)
					else:
						channeladd = guild.get_channel(589942497678196764)# 590664052318142474
					await channeladd.set_permissions(rolesearch, overwrite=discord.PermissionOverwrite(read_messages=True))
					desc += "Ajout d'un nouveau jeu dans la catégorie {}: {}".format(channeladd.mention, rolesearch.mention)
					channel = guild.get_channel(417449076775321600)
				msg = discord.Embed(title = "Création de jeu",color= 13752280, description = desc)
				await ctx.channel.send(embed = msg)
			else:
				await ctx.channel.send("Le jeu "+game+" existe déjà")
		else :
			await ctx.channel.send("Tu ne peux pas exécuter cette commande.")



	@commands.command(pass_context=True)
	async def gameadd(self, ctx, role, nom = None):
		"""**[role]** | Permet de s'ajouter des roles (Pour les Inquisiteurs, mentionner l'utilisateur cible apres le role pour lui affecter)"""
		if ge.permission(ctx, ge.Joueurs)==True:
			if nom != None:
				if ge.permission(ctx, ge.Inquisiteur)==True:
					ID = DB.nom_ID(nom)
					nom = ctx.guild.get_member(ID)
					nom = nom.name
				else:
					await ctx.channel.send("Tu peux exécuter cette commande uniquement pour toi.")
					return
			else:
				ID = ctx.author.id
				nom = ctx.author.name
			user = get(ctx.guild.members, id=ID)
			if user:
				setrole = get(user.guild.roles, name=role)
				if ge.permission(ctx, ge.Inquisiteur, ctx.author)==False:
					for i in range(0,len(rolelist)):
						if role == rolelist[i]:
							await ctx.channel.send("Tu ne peux pas exécuter cette commande avec ce role.")
							return
				await user.add_roles(setrole)
				desc = "Le role `{}` a été ajouté à {}".format(role, nom)
				msg = discord.Embed(title = "Ajout de jeu",color= 13752280, description = desc)
				await ctx.channel.send(embed = msg)
				return
			else:
				await ctx.channel.send("L'utilisateur n'as pas été trouvé.")
		else:
			await ctx.channel.send("Tu ne peux pas exécuter cette commande.")



	@commands.command(pass_context=True)
	async def gameremove(self, ctx, role, nom = None):
		"""**[role]** | Permet de s'enlever des roles (Pour les Inquisiteurs, mentionner l'utilisateur cible apres le role pour lui enlever)"""
		if ge.permission(ctx, ge.Joueurs)==True:
			if nom != None:
				if ge.permission(ctx, ge.Inquisiteur)==True:
					ID = DB.nom_ID(nom)
					nom = ctx.guild.get_member(ID)
					nom = nom.name
				else:
					await ctx.channel.send("Tu peux exécuter cette commande uniquement pour toi.")
					return
			else:
				ID = ctx.author.id
				nom = ctx.author.name
			user = get(ctx.guild.members, id=ID)
			if user:
				setrole = get(user.guild.roles, name=role)
				await user.remove_roles(setrole)
				desc = "Le role `{}` a été enlevé à {}".format(role, nom)
				msg = discord.Embed(title = "Retrait de jeu",color=9109504, description = desc)
				await ctx.channel.send(embed = msg)
				return
			else:
				await ctx.channel.send("L'utilisateur n'as pas été trouvé.")
		else:
			await ctx.channel.send("Tu ne peux pas exécuter cette commande.")



	@commands.command(pass_context=True)
	async def gamelist(self, ctx):
		"""Affiche la liste des jeux"""
		desc = ""
		jsonlist = ctx.guild.roles
		# print(jsonlist)
		for i in range(2, len(jsonlist)-14):
			desc += "{}\n".format(jsonlist[i])
		msg = discord.Embed(title = "Liste des jeux",color=35723, description = desc)
		await ctx.channel.send(embed = msg)


def setup(bot):
	bot.add_cog(Roles(bot))
	open("fichier_txt/cogs.txt","a").write("Roles\n")
