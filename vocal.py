import discord
from discord.ext import commands
import DB
import youtube_dl
import os
import asyncio
from youtube import youtube_top_link, search_youtube, get_youtube_url

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

class Info():
	def __init__(self):
		self.url = []
		self.title = []
		self.ydl_opt ={
			'format':'bestaudio/best',
			'postprocessors':
				[{
				'key':'FFmpegExtractAudio',
				'preferredcodec':'mp3',
				'preferredquality':'192',
				}]
		}
	def add(self,url):
		self.url.append(url)
		with youtube_dl.YoutubeDL(self.ydl_opt) as ydl:
			self.info = ydl.extract_info(url,download = False)
		self.title.append(self.info.get('title',None))

	def sup(self):
		del self.url[0]
		del self.title[0]

	def last_title(self):
		n = len(self.url)-1
		return (self.title[n])

	def last_url(self):
		n = len(self.url)-1
		return (self.url[n])

	def purge(self):
		self.url = []
		self.title = []

class Queue(commands.Cog):

	def __init__(self,bot):
		self.bot = bot
		self.info = Info()

	async def add_to_queue(self, ctx, url):
		self.info.add(url)
		if not ctx.voice_client.is_playing():
			await ctx.send("downloading file")
			self.dl(url)
			song = discord.FFmpegPCMAudio("song.mp3")
			ctx.voice_client.play(song, after =lambda e: self.next(ctx))
			await ctx.send("{} se lance".format(self.info.title[0]))
		else:
			await ctx.send("{} ajouté à la queue".format(self.info.last_title()))
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
				print("renamed File:{}".format(file))
				os.rename(file,"song.mp3")

	def next(self,ctx):
		try :
			self.info.sup()
		except ValueError:
			print("liste vide")
			pass
		if not self.info.url:
			msg = 'la queue est vide'
			print('la queue est vide')
		else:
			msg = 'lecture de {}'.format(self.info.title[0])
			self.dl (self.info.url[0])
			ctx.voice_client.play(discord.FFmpegPCMAudio("song.mp3"), after =lambda e: self.next(ctx))
		envoie = ctx.send(msg)
		fut = asyncio.run_coroutine_threadsafe(envoie, self.bot.loop)
		try:
			fut.result()
		except:
			# an error happened sending the message
			pass

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
		self.music.info.purge()
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

		await self.music.add_to_queue(ctx,url)

	@commands.command(pass_context=True)
	async def skip(self, ctx):
		"""permet de passer la chanson en cours"""
		voice = ctx.voice_client
		if voice.is_connected():
			if permission(ctx,Ambassadeur):
				voice.stop()
				await ctx.send("music skipped")
			else:
				if ctx.author.id in self.skip:
					return
				else:
					self.skip.append(ctx.author.id)
					n = len(self.skip)
					m = len(ctx.author.voice.channel.members)-1
					print(n,m)
					if n >= m/2:
						voice.stop()
						await ctx.send("music skipped")
						self.skip = []
					else:
						await ctx.send("il manque {} joueur.s pour skip".format(round(m/2)-n))
		else:
			return

	@commands.command(pass_context=True)
	async def list(self, ctx):
		"""donne la liste des musiques dans la queue"""
		self.list = self.music.info.title
		desc = "*en cours* : {}\n".format(self.list[0])
		self.list = self.list[1:]
		if self.list :
			i = 1
			for song in self.list:
				desc += "-{} {}\n".format(i,song)
				i+=1
		msg = discord.Embed(title = "Listes des musiques dans la liste",color= 12745742, description = desc)
		await ctx.send(embed = msg, delete_after = 60)

	@commands.command(pass_context=True)
	async def search(self, ctx,*,args):
		"""Donne les 5 premiers résultats de ta recherche sur youtube ! """
		result = search_youtube(user_input=args, number=5)
		embed = discord.Embed(color=0xFF0000)
		embed.set_footer(text="Tapez un nombre pour faire votre choix "
							  "ou dites \"cancel\" pour annuler")
		for s in result:
			url = get_youtube_url(s)
			embed.add_field(name="{}.{}".format(result.index(s)+1,s['type']),
							value="[{}]({})".format(s['title'],url), inline=False)
		self_message = await ctx.send(embed=embed)

		def check(message):
			return message.author == ctx.author
		try:
			msg = await self.bot.wait_for("message", check=check, timeout=15)
			if msg.content == "cancel":
				await ctx.send("Annulé !", delete_after=5)
				await self_message.delete(delay=None)
				await ctx.message.delete(delay=2)
				await msg.delete(delay=1)
			else:
				num = int(msg.content)
				if num > 0 and num <= len(result):
					url = get_youtube_url(result[num - 1])
					await ctx.send(content="{}".format(url))
					await ctx.message.delete(delay=2)
					await self_message.delete(delay=None)
					await msg.delete(delay=1)


		except asyncio.TimeoutError:
			await ctx.send("Tu as pris trop de temps pour répondre !", delete_after=5)
			await self_message.delete(delay=None)
			await ctx.message.delete(delay=2)

def setup(bot):
	bot.add_cog(Music(bot))
	open("fichier_txt/cogs.txt","a").write("Music\n")
