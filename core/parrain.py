from DB import TinyDB as DB
from discord.ext import commands, tasks
from discord.ext.commands import bot
from discord.utils import get
import discord
from core import welcome as wel

client = discord.Client()

#===============================================================

class Parrain(commands.Cog):

	def __init__(self,bot):
		return (None)

	@commands.command(pass_context=True)
	async def parrain(self, ctx, nom=None):
		"""
		Permet d'ajouter un joueur comme parrain.
		En le faisant vous touchez un bonus et lui aussi
		"""
		if ctx.guild.id == wel.idBASTION:
			ID = ctx.author.id
			if nom != None :
				ID_p = DB.nom_ID(nom)
				if DB.userExist(ID_p) == True and DB.valueAt(ID, "parrain") == 0 and ID_p != ID:
					DB.updateField(ID, "parrain", ID_p)
					print("Parrain ajouté")
					fil_L = DB.valueAt(ID_p, "filleul")
					fil_L.append(ID)
					DB.updateField(ID_p, "filleul", fil_L)
					DB.addGems(ID, 50)
					gain_p = 100 * len(fil_L)
					DB.addGems(ID_p, gain_p)
					msg = "Votre parrain a bien été ajouté ! Vous empochez 50 :gem: et lui "+str(gain_p)+" :gem:."
				else :
					print("Impossible d'ajouter ce joueur comme parrain")
					msg = "Impossible d'ajouter ce joueur comme parrain"

			await ctx.channel.send(msg)
		else:
			await ctx.channel.send("commande utilisable uniquement sur le discord `Bastion`")

	@commands.command(pass_context=True)
	async def filleul(self, ctx, nom=None):
		"""
		Affiche la liste des filleuls d'un joueur
		"""
		if ctx.guild.id == wel.idBASTION:
			if nom == None:
				ID = ctx.author.id
				Nom = ctx.author.name
			else :
				ID = DB.nom_ID(nom)
				if ID == -1:
					msg = "Ce joueur n'existe pas !"
					await ctx.channel.send(msg)
					return

			F_li = DB.valueAt(ID, "filleul")
			if len(F_li) > 0:
				if len(F_li)>1:
					sV = "s"
				else:
					sV= ""
				msg="Filleul{1} `x{0}`:".format(len(F_li),sV)
				for one in F_li:
					msg+="\n<@"+str(one)+">"
				emb = discord.Embed(title = "Informations :",color= 13752280, description = msg)
				await ctx.channel.send(embed = emb)
			else:
				msg = "Vous n'avez pas de filleul, invitez de nouveaux joueurs !"
				await ctx.channel.send(msg)
		else:
			await ctx.channel.send("commande utilisable uniquement sur le discord `Bastion`")

def setup(bot):
	bot.add_cog(Parrain(bot))
	open("help/cogs.txt","a").write("Parrain\n")
