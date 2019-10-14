import discord
from discord.ext import commands
from discord.ext.commands import bot
from discord.utils import get
import random as r
from core import welcome as wel
from google_images_download import google_images_download

response = google_images_download.googleimagesdownload()


import os.path
from os import scandir


class Counter(object):
	""" Classe qui gère le listage et le comptage de chaque dossier. """

	def __init__(self, path):
		""" Initialisation des variables. """

		if not path:
			raise ValueError('A girl needs a path.')

		self.path = path
		self.files = 0

	def work(self):
		""" La méthode qui scanne le dossier et fait le décompte. """

		# `entry` contient pas mal d'informations. Voir :
		#  https://docs.python.org/3/library/os.html#os.DirEntry
		for entry in scandir(self.path):

			# S'il s'agit d'un dossier qui n'est pas un lien symbolique...
			if entry.is_dir() and not entry.is_symlink():

				# ... On instancie une autre classe de `Counter` afin de faire
				# le décompte des fichiers de ce dossier.
				path = os.path.join(self.path, entry.name)
				counter = Counter(path)

				# `yield from` permet de capter et renvoyer le `yield self` du
				# compteur que l'on vient d'instancier. Pour faire plus simple,
				# on récupère la classe une fois que le décompte du dossier
				# est terminé.
				yield from counter.work()
			else:
				# Il s'agit d'un fichier, on incrémente le compteur.
				self.files += 1

		# On renvoie la classe elle-même. On pourrait aussi renvoyer seulement
		# les infos nécessaires avec un `yield (self.path, self.files)`.
		yield self

	def __str__(self):
		""" Représentation de la classe. Permet de faire :
			>>> print(cls)
			/etc 115
		"""

		return '{} {}'.format(self.path, self.files)



def images_url(k, nb):
	"""
	Télécharge les images demandées dans le dossier downloads
	"""
	arguments = {"keywords":k,"limit":nb,"print_urls":True,"size":"medium","silent_mode":True,"safe_search":True,"no_download":True}   #creating list of arguments
	paths = response.download(arguments)
	return paths

def images_url_nsfw(k, nb):
	"""
	Télécharge les images demandées dans le dossier downloads
	"""
	arguments = {"keywords":k,"limit":nb,"print_urls":True,"size":"medium","silent_mode":True,"no_download":True}   #creating list of arguments
	paths = response.download(arguments)
	return paths


class Images(commands.Cog):

	def __init__(self,ctx):
		return(None)


	@commands.command(pass_context=True)
	async def img(self, ctx, keyword, nbfiles = 20, choise_nbfile = None):
		"""
		**[mots clés]** _{nb image max} {numéro image}_ | Affiche une image en fonction des mots clés
		"""
		if nbfiles < 5:
			nbfiles = 20
		if choise_nbfile != None:
			choise_nbfile = int(choise_nbfile)
			if choise_nbfile > int(nbfiles) or choise_nbfile < 1:
				choise_nbfile = None
		else:
			choise_nbfile=r.randint(1, nbfiles)

		url = images_url(keyword, nbfiles)
		url2 = url[0][keyword][choise_nbfile]
		await ctx.channel.send(url2)


	@commands.command(pass_context=True)
	async def nsfw(self, ctx, keyword):
		"""
		**[mots clés]** _{nb image max} {numéro image}_ | Affiche une image en fonction des mots clés
		"""
		if ctx.channel.id == wel.idchannel_nsfw or ctx.channel.id == 627968844274860073 :
			if nbfiles < 5:
				nbfiles = 20
			if choise_nbfile != None:
				choise_nbfile = int(choise_nbfile)
				if choise_nbfile > int(nbfiles) or choise_nbfile < 1:
					choise_nbfile = None
			else:
				choise_nbfile=r.randint(1, nbfiles)

			url = images_url(keyword, nbfiles)
			url2 = url[0][keyword][choise_nbfile]
			await ctx.channel.send(url2)
		else:
			await ctx.channel.send("Tu ne peux pas utilisé cette commande dans ce salon")



class ImagesSecret(commands.Cog):

	def __init__(self,ctx):
		return(None)


	@commands.command(pass_context=True)
	async def raclette(self, ctx):
		keyword = "raclette"
		nbfiles = 20
		choise_nbfile=r.randint(1, nbfiles)
		url = images_url(keyword, nbfiles)
		url2 = url[0][keyword][choise_nbfile]
		await ctx.channel.send(url2)



def setup(bot):
	bot.add_cog(Images(bot))
		bot.add_cog(ImagesSecret(bot))
	open("help/cogs.txt","a").write("Images\n")
