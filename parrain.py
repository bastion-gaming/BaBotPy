import DB
from discord.ext import commands, tasks
from discord.ext.commands import bot
from discord.utils import get
import discord

client = discord.Client()


def addGems(ID, nbGems):
	"""
	Permet d'ajouter un nombre de gems à quelqu'un. Il nous faut son ID et le nombre de gems.
	Si vous souhaitez en retirer mettez un nombre négatif.
	Si il n'y a pas assez d'argent sur le compte la fonction retourne un nombre
	strictement inférieur à 0.
	"""
	old_value = DB.valueAt(ID, "gems")
	new_value = int(old_value) + nbGems
	if new_value >= 0:
		DB.updateField(ID, "gems", new_value)
		# print("Le compte de "+str(ID)+ " est maintenant de: "+str(new_value))
	# else:
	# 	print("Il n'y a pas assez sur ce compte !")
	return str(new_value)

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
				addGems(ID, 50)
				addGems(ID_p, 100 * len(fil_L))
				msg = "Votre parrain a bien été ajouté ! Vous empochez 50 et lui 100 plus son multiplicateur"
			else :
				print("Impossible d'ajouter ce joueur comme parrain")
				msg = "Impossible d'ajouter ce joueur comme parrain"

		await ctx.channel.send(msg)

def setup(bot):
	bot.add_cog(Parrain(bot))
	open("fichier_txt/cogs.txt","a").write("Parrain\n")
