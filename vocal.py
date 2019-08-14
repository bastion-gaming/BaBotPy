import discord
from discord.ext import commands
import DB
import youtube_dl
import os


admin = 0
Inquisiteur = 1
Ambassadeur = 2
perm = [["Baron du Bastion"],["Baron du Bastion","Inquisiteur du Bastion"],["Inquisiteur du Bastion","Baron du Bastion","Ambassadeur"]]
def permission(ctx,grade):
	roles = ctx.author.roles
	for role in roles :
		if role.name in perm[grade]:
			return(True)
	return(False)

class Queue(commands.Cog):

	def __init__(self,bot):
		self.bot = bot
		self.url = []

	async def add_to_queue(self, ctx, url):
		self.url.append(url)
		if not ctx.voice_client.is_playing():
			self.dl(url)
			ctx.voice_client.play(discord.FFmpegPCMAudio("song.mp3"), after =lambda e: self.next(ctx))
			await ctx.send("{} se lance".format(self.name))
		else:
			await ctx.send("ajouté à la queue")
			# print("ajouté à la queue")
	def dl(self, url):
		ydl_opts ={
			'format':'bestaudio/best',
			'postprocessors':
				[{
				'key':'FFmpegExtractAudio',
				'preferredcodec':'mp3',
				'preferredquality':'192',
				}]
		}
		with youtube_dl.YoutubeDL(ydl_opts) as ydl:
			print('Downloading song now;\n')
			ydl.download([url])

		for file in os.listdir('./'):
			if file.endswith(".mp3"):
				self.name = file
				print("renamed File:{}".format(file))
				os.rename(file,"song.mp3")

	def next(self,ctx):
		if not self.url:
			print('la queue est vide')
		else:
			del self.url[0]
			self.dl (self.url[0])
			ctx.voice_client.play(discord.FFmpegPCMAudio("song.mp3"), after =lambda e: self.next(ctx))


class Music(commands.Cog):

	def __init__(self,bot):
		self.bot = bot
		self.skip = []
		self.music = Queue(self.bot)

	@commands.command(pass_context=True)
	async def join(self, ctx):
		"""le bot rejoint le channel vocal """
		try :
			vocal = ctx.author.voice.channel
			print([y.name for y in vocal.members])
			await vocal.connect(timeout=60.0, reconnect=True)
		except :
			await ctx.channel.send("Il faut d'abord se connecter dans un channel vocal !")
			pass

	@commands.command(pass_context=True)
	async def leave(self, ctx):
		"""le bot quitte le channel vocal """
		voice = ctx.voice_client
		voice.stop()
		await voice.disconnect()

	@commands.command(pass_context=True)
	async def play(self, ctx, url):
		"""Le bot joue la vidéo youtube (url uniquement)"""
		voice = ctx.voice_client
		song_there = os.path.isfile("song.mp3")
		try :
			if song_there:
				os.remove('song.mp3')
				print('removed old song file')

		except PermissionError:
			print('trying to delete the song file')
			ctx.send("ERROR music playing")
			return

		await ctx.send("getting everything ready now")
		await self.music.add_to_queue(ctx,url)

	@commands.command(pass_context=True)
	async def skip(self, ctx):
		voice = ctx.voice_client
		if voice.is_connected():
			if permission(ctx,Ambassadeur):
				voice.stop()
				self.music.next(ctx)
				ctx.send("music skipped")
			else:
				if ctx.member.id in self.skip:
					return
				else:
					self.skip.append(ctx.member.id)
					n = len(self.skip)
					m = len(ctx.author.voice.channel.members)
					if n >= m/2:
						voice.stop()
						self.music.next(ctx)
						ctx.send("music skipped")
					else:
						ctx.send("il manque {} joueur.s pour skip".format(round((m/2)-n)))
		else:
			return


def setup(bot):
	bot.add_cog(Music(bot))
	open("fichier_txt/cogs.txt","a").write("Music\n")
