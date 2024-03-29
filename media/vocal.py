import discord
from discord.ext import commands
from discord.utils import get
import youtube_dl
import os
import asyncio
from media.youtube import search_youtube, get_youtube_url
from core import gestion as ge


class Info():

    def __init__(self):
        self.url = []
        self.title = []
        self.ydl_opt = {
            'format': 'bestaudio/best',
            'postprocessors':
                [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }]
        }

    def add(self, url):
        self.url.append(url)
        with youtube_dl.YoutubeDL(self.ydl_opt) as ydl:
            self.info = ydl.extract_info(url, download = False)
        self.title.append(self.info.get('title', None))

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

    def __init__(self, bot):
        self.bot = bot
        self.info = Info()

    async def add_to_queue(self, ctx, url):
        self.info.add(url)
        if not ctx.voice_client.is_playing():
            await ctx.send("downloading file")
            self.dl(url)
            song = discord.FFmpegPCMAudio("core/cache/song.mp3")
            ctx.voice_client.play(song, after =lambda e: self.next(ctx))
            await ctx.send("{} se lance".format(self.info.title[0]))
        else:
            await ctx.send("{} ajouté à la queue".format(self.info.last_title()))
            print("Media >> ajouté à la queue")

    def dl(self, url):
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': 'core/cache/song.mp3',
            'postprocessors':
                [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }]
        }
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            print('Media >> Downloading song now;\n')
            ydl.download([url])

    def next(self, ctx):
        try :
            self.info.sup()
        except ValueError:
            print("Media >> liste vide")
            pass
        if not self.info.url:
            msg = 'la queue est vide'
            print('Media >> la queue est vide')
        else:
            song_there = os.path.isfile("core/cache/song.mp3")
            try :
                if song_there:
                    os.remove('core/cache/song.mp3')
                    print('Media >> removed old song file')
            except PermissionError:
                print('Media >> trying to delete the song file')
                ctx.send("ERROR music playing")
                pass

            msg = 'lecture de {}'.format(self.info.title[0])
            self.dl(self.info.url[0])
            ctx.voice_client.play(discord.FFmpegPCMAudio("core/cache/song.mp3"), after =lambda e: self.next(ctx))
        envoie = ctx.send(msg)
        fut = asyncio.run_coroutine_threadsafe(envoie, self.bot.loop)
        try:
            fut.result()
        except:
            # an error happened sending the message
            pass


class Music(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.client = bot
        self.skip = []
        self.music = Queue(self.bot)

    @commands.command(pass_context=True)
    async def join(self, ctx):
        """Le bot rejoint le channel vocal """
        try:
            channel = ctx.author.voice.channel
            # print([y.name for y in vocal.members])
            vocal = discord.utils.get(ctx.guild.voice_channels, name=channel.name)
            vocal_client = discord.utils.get(self.client.voice_clients, guild=ctx.guild)

            if vocal_client == None:
                await channel.guild.change_voice_state(channel=channel, self_deaf=True)
                await vocal.connect(timeout=60.0, reconnect=True)
            else:
                await vocal_client.move_to(channel)
        except:
            await ctx.channel.send("Il faut d'abord se connecter dans un channel vocal !")
            pass

    @commands.command(pass_context=True)
    async def leave(self, ctx):
        """Le bot quitte le channel vocal """
        voice = ctx.voice_client
        song_there = os.path.isfile("cache/song.mp3")
        try :
            if song_there:
                os.remove('core/cache/song.mp3')
                print('Media >> removed old song file')

        except PermissionError:
            print('Media >> trying to delete the song file')
            ctx.send("ERROR music playing")
            return
        self.music.info.purge()
        voice.stop()
        await voice.disconnect()

    @commands.command(pass_context=True)
    async def play(self, ctx, url):
        """**[url]** | Le bot joue la vidéo youtube (url uniquement)"""
        song_there = os.path.isfile("core/cache/song.mp3")
        try :
            if song_there:
                os.remove('core/cache/song.mp3')
                print('Media >> removed old song file')

        except PermissionError:
            print('Media >> trying to delete the song file')
            ctx.send("ERROR music playing")
            return

        try:
            channel = ctx.author.voice.channel
            # print([y.name for y in vocal.members])
            vocal = discord.utils.get(ctx.guild.voice_channels, name=channel.name)
            vocal_client = discord.utils.get(self.client.voice_clients, guild=ctx.guild)

            if vocal_client == None:
                await channel.guild.change_voice_state(channel=channel, self_deaf=True)
                await vocal.connect(timeout=60.0, reconnect=True)
            else:
                await vocal_client.move_to(channel)
        except:
            await ctx.channel.send("Il faut d'abord se connecter dans un channel vocal !")
        await self.music.add_to_queue(ctx, url)

    @commands.command(pass_context=True)
    async def skip(self, ctx):
        """Permet de passer la chanson en cours"""
        voice = ctx.voice_client
        if voice.is_connected():
            if ge.permission(ctx, ge.Inquisiteur):
                voice.stop()
                await ctx.send("music skipped")
            else:
                if ctx.author.id in self.skip:
                    return
                else:
                    self.skip.append(ctx.author.id)
                    n = len(self.skip)
                    m = len(ctx.author.voice.channel.members)-1
                    # print(n, m)
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
        """Donne la liste des musiques dans la queue"""
        self.list = self.music.info.title
        desc = "*en cours* : {}\n".format(self.list[0])
        self.list = self.list[1:]
        if self.list :
            i = 1
            for song in self.list:
                desc += "-{} {}\n".format(i, song)
                i += 1
        msg = discord.Embed(title = "Listes des musiques dans la liste", color= 12745742, description = desc)
        await ctx.send(embed = msg, delete_after = 60)

    @commands.command(pass_context=True)
    async def search(self, ctx, *, args):
        """**[recherche]** | Donne les 5 premiers résultats de ta recherche sur youtube ! """
        result = search_youtube(user_input=args, number=5)
        embed = discord.Embed(color=0xFF0000)
        embed.set_footer(text="Tapez un nombre pour faire votre choix "
                              "ou dites \"cancel\" pour annuler")
        for s in result:
            url = get_youtube_url(s)
            embed.add_field(name="{}.{}".format(result.index(s)+1, s['type']),
                            value="[{}]({})".format(s['title'], url), inline=False)
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
                    await self.music.add_to_queue(ctx, url)
                    await ctx.message.delete(delay=2)
                    await self_message.delete(delay=None)
                    await msg.delete(delay=1)

        except asyncio.TimeoutError:
            await ctx.send("Tu as pris trop de temps pour répondre !", delete_after=5)
            await self_message.delete(delay=None)
            await ctx.message.delete(delay=2)


def setup(bot):
    bot.add_cog(Music(bot))
    open("core/cache/cogs.txt", "a").write("Music\n")
