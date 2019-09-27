import discord
from discord.ext import commands
from discord.ext.commands import bot
from discord.utils import get
import random as r
from google_images_download import google_images_download   #importing the library

response = google_images_download.googleimagesdownload()   #class instantiation


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



def images_download(k):
	arguments = {"keywords":k,"limit":20,"print_urls":False,"size":"medium","silent_mode":True,"safe_search":True}   #creating list of arguments
	paths = response.download(arguments)   #passing the arguments to the function
	print(paths)   #printing absolute paths of the downloaded images


class Images(commands.Cog):

	def __init__(self,ctx):
		return(None)


	@commands.command(pass_context=True)
	async def img(self, ctx, keyword):
		"""
		"""
		nbfiles = 0
		images_download(keyword)
		counter = Counter("downloads/{}".format(keyword))
		for cls in counter.work():
			# Afficher seulement les dossiers non vides
			if cls.files:
				nbfiles = cls.files
		if nbfiles != 0:
			choise_nbfile=r.randint(1, nbfiles)
			listfiles=os.listdir("downloads/{}".format(keyword))
		await ctx.channel.send(file=discord.File("downloads/{0}/{1}".format(keyword, listfiles[choise_nbfile])))
		contenu=os.listdir('downloads/{}'.format(keyword))
		for x in contenu:
		   os.remove('downloads/{0}/{1}'.format(keyword, x))#on supprime tous les fichier dans le dossier
		os.rmdir('downloads/{}'.format(keyword))#puis on supprime le dossier



def setup(bot):
	bot.add_cog(Images(bot))
	open("fichier_txt/cogs.txt","a").write("Images\n")
