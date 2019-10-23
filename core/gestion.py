import discord
import random as r
import time as t
from discord.ext import commands
from discord.ext.commands import Bot
from discord.utils import get
import time
import asyncio
from DB import DB
from core import welcome as wel

PREFIX = open("core/prefix.txt","r").read().replace("\n","")
client = Bot(command_prefix = "{0}".format(PREFIX))

admin = 0
Inquisiteur = 1
Ambassadeur = 2
Joueurs = 3
perm = [["Baron du Bastion"],["Baron du Bastion","Inquisiteur du Bastion"],["Inquisiteur du Bastion","Baron du Bastion","Ambassadeur"],["Inquisiteur du Bastion","Baron du Bastion","Ambassadeur","Joueurs"]]
choix_G =[[':regional_indicator_a:','🇦',0],[':regional_indicator_b:','🇧',0],[':regional_indicator_c:','🇨',0],[':regional_indicator_d:','🇩',0],[':regional_indicator_e:','🇪',0]]
def permission(ctx,grade,author = None):
	if not author :
		roles = ctx.author.roles
		for role in roles :
			if role.name in perm[grade] or ctx.guild.id == 478003352551030796:
				return(True)
	else :
		roles = author.roles
		for role in roles :
			if role.name in perm[grade] or ctx.guild.id == 478003352551030796:
				return(True)
	return(False)

class Gestion(commands.Cog):

	def __init__(self,bot):
		self.bot = bot
		return

	@commands.command(pass_context=True)
	async def show_perm(self, ctx):
		"""Montre les permissions et leur valeurs"""
		msg = "Voici tes roles :```"
		roles = ctx.author.roles
		for role in roles:
			msg +="~ {} à pour valeur :{}\n".format(role.name,role.permissions.value)
		msg += "```"
		await ctx.channel.send(msg)

	@commands.command(pass_context=True)
	async def getmember(self, ctx):
		"""Update de la BDD"""
		if ctx.guild.id == wel.idBASTION:
			if permission(ctx,Inquisiteur):
				members = ctx.guild.members
				for member in members:
					DB.newPlayer(member.id)
				await ctx.channel.send("la bdd est remplis !")
			else:
				ctx.send("tu n'as pas les droits")
		else:
			await ctx.channel.send("commande utilisable uniquement sur le discord `Bastion`")

	@commands.command(pass_context=True)
	async def supp(self, ctx, nb):
		"""**[nombre]** | Supprime [nombre] de message dans le channel """
		if permission(ctx,Inquisiteur):
			try :
				nb = int(nb)
				if nb <= 20 :
					await ctx.channel.purge(limit =nb)
					msg ='{0} messages on été éffacé !'.format(nb)
				else:
					msg = "on ne peut pas supprimer plus de 20 message à la fois"
			except ValueError:
				msg = "commande mal remplis"
		else :
			msg = "tu ne remplis pas les conditions"
		await ctx.channel.send(msg)

	@client.command(pass_context=True)
	async def vote(self, ctx, *, args):
		"""
		**[durée]//[thème du vote]//[choix 1]/[choix 2]/<etc> ** | Créé un vote pendant 1h !
		"""
		if permission(ctx,Ambassadeur):
			choix = choix_G[:]
			args = args.split("//")
			temps = float(args[0])*3600
			question = args[1]
			props = args[2].split("/")
			desc = ""
			n = len(props)
			if n>5:
				await ctx.channel.send("5 choix sont possible au maximum!")
				return(None)
			msg = discord.Embed(title = "Un nouveau vote est lancé !",color= 12745742, description = question)
			for i in range(n):
				desc += "{} {} : {} vote(s)\n".format(choix[i][0],props[i],choix[i][2])
			desc += ":x: annuler son vote\n"
			msg.add_field(name="les différents choix", value=desc, inline=False)
			mess = await ctx.channel.send(embed=msg)
			for i in range(len(props)):
				await mess.add_reaction(choix[i][1])
			await mess.add_reaction('❌')
			t_init = time.time()
			votant ={}
			global exit
			exit = True

			def check (reaction,user):
				if user == client.user :
					return(False)
				if reaction.emoji == '🛑':
					print(user.name)
					if permission(ctx,Ambassadeur,user):
						global exit
						exit = False
						return(False)
					else:
						print('pas les droits')
						return(False)

				elif user in votant :
					if reaction.emoji == '❌':
						emoji = votant[user]
						for i in range(n):
							if emoji == choix[i][1]:
								choix[i][2] -= 1
						del votant[user]
						return(True)
					else:
						return(False)
				else :
					votant[user] = reaction.emoji
					for i in range(n):
						if reaction.emoji == choix[i][1]:
							choix[i][2] += 1
					return(True)
			while t_init + temps > time.time() and exit:
				print(exit)
				try :
					reaction, user = await self.bot.wait_for('reaction_add', timeout=10, check = check)
					msg = discord.Embed(title = "Un nouveau vote est lancé !",color= 12745742, description = question)
					desc = ""
					for i in range(n):
						desc += "{} {} : {} vote(s)\n".format(choix[i][0],props[i],choix[i][2])
					desc += ":x: annuler son vote\n"
					msg.add_field(name="les différents choix", value=desc, inline=False)
					await mess.edit(embed = msg)
				except asyncio.TimeoutError:
					print('60 sec ont passé')
					pass
			max = 0
			for i in range (n):
				if choix[i][2] > max :
					max = choix[i][2]
					gagnant_nom = props[i]
					gagnant_votes = max
				elif choix[i][2] == max :
					gagnant_nom = "égalité"
					gagnant_votes = max

			msg2 = "Fin des votes !\nLe gagnant des votes : **{}** avec **{}** votes !".format(gagnant_nom,gagnant_votes)
			await ctx.channel.send(msg2)
		else:
			await ctx.send("tu n'as pas la permission de faire ça !")

def setup(bot):
	bot.add_cog(Gestion(bot))
	open("help/cogs.txt","a").write("Gestion\n")
