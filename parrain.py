import DB
from discord.ext import commands, tasks
from discord.ext.commands import bot
from discord.utils import get
import discord

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

def setup(bot):
	bot.add_cog(Parrain(bot))
	open("fichier_txt/cogs.txt","a").write("Parrain\n")
