import discord
from discord.ext import commands
import gestion as ge

async def addrole(member, role):
	setrole = discord.utils.get(member.guild.roles, name=role)
	await member.add_roles(setrole)

class Roles(commands.Cog):

	def __init__(self,ctx):
		return(None)

	@commands.command(pass_context=True)
	async def creategame(self, ctx, game, categorie):
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
				msg = "Le jeu '"+game+"' a été créé"

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
					msg = "Ajout d'un nouveau jeu dans la catégorie {}: {}".format(channeladd.mention, rolesearch.mention)
					channel = guild.get_channel(417449076775321600)
					return (ctx.channel.send(msg))
				else:
					await ctx.channel.send(msg)
			else:
				await ctx.channel.send("Le jeu "+game+" existe déjà")
		else :
			await ctx.channel.send("Tu ne peux pas exécuter cette commande.")


def setup(bot):
	bot.add_cog(Roles(bot))
	open("fichier_txt/cogs.txt","a").write("Roles\n")
