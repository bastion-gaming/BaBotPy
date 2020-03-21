from discord.ext import commands
from discord.ext.commands import bot
import discord
from core import welcome as wel, gestion as ge
from DB import SQLite as sql

ServIDmoji = 634317171496976395
nb_saisons = 0
date_saison = ""
client = discord.Client()
VERSION = open("core/version.txt").read().replace("\n", "")


class Utils(commands.Cog):

    def __init__(self, ctx):
        return(None)

    @commands.command(pass_context=True)
    async def version(self, ctx):
            """
            Permet d'avoir la version du bot.
            """
            msg = "Je suis en version : **{0}**.".format(VERSION)
            await ctx.channel.send(msg)

    @commands.command(pass_context=True)
    async def site(self, ctx):
            """
            Permet d'avoir le site de bastion.
            """
            msg = "Le site est : **http://www.bastion-gaming.fr/**."
            await ctx.channel.send(msg)

    @commands.command(pass_context=True)
    async def ping(self, ctx):
            """
            PONG.
            """
            msg = "**PONG**."
            await ctx.channel.send(msg)

    @commands.command(pass_context=True)
    async def twitch(self, ctx):
            """
            Permet d'avoir le lien du twitch.
            """
            msg = "Notre chaine twitch :arrow_right: **https://www.twitch.tv/bastionautes/**."
            await ctx.channel.send(msg)

    # @commands.command(pass_context=True)
    # async def agenda(self, ctx):
    #         """
    #         Permet d'avoir le lien de l'agenda.
    #         """
    #         msg = "Notre agenda :arrow_right: **http://www.bastion-gaming.fr/agenda.html**."
    #         await ctx.channel.send(msg)

    @commands.command(pass_context=True)
    async def github(self, ctx):
            """
            Permet d'avoir le lien du github.
            """
            msg = "Le github du Bot :arrow_right: **https://github.com/bastion-gaming/bot-discord**."
            await ctx.channel.send(msg)

    @commands.command(pass_context=True)
    async def usercount(self, ctx):
        """
        Affiche le nombre d'utilisateurs inscrit dans la base de données
        """
        if ctx.guild.id == wel.idBASTION:
            len = sql.taille("IDs")
            if len == 0:
                await ctx.channel.send("Aucun utilisaeur enregistrer dans la base de donées")
            else:
                await ctx.channel.send("{} utilisateur inscrit".format(len))
        else:
            await ctx.channel.send("Commande utilisable uniquement sur le discord `Bastion`")


class UtilsSecret(commands.Cog):

    def __init__(self, ctx):
        return(None)

    @commands.command(pass_context=True)
    async def test(self, ctx, ID = None, arg1 = None, arg2 = None, arg3 = None, arg4 = None):
        if ID == "check":
            await ctx.channel.send("Check!")
        # elif ID == "stat":
        #     if arg1 == "write":
        #         await ctx.channel.send(GS.csv_add(arg2))
        #     elif arg1 == "read":
        #         await ctx.channel.send(GS.csv_read(arg2, dt.datetime.now()))
        else:
            await ctx.channel.send(":regional_indicator_t::regional_indicator_e::regional_indicator_s::regional_indicator_t:")

    @commands.command(pass_context=True)
    async def sql(self, ctx, fct = None, ID = None, arg2 = None, arg3 = None, arg4 = None):
        if ID == None:
            ID = ctx.author.id
        else:
            try:
                ID = int(ID)
            except:
                ID = sql.nom_ID(ID)
        if ge.permission(ctx, ge.admin):
            if fct == "init":
                sql.init()
            elif fct == "begin":
                if arg2 == "bastion":
                    msg = sql.newPlayer(ID, arg2)
                else:
                    msg = "DB inconnu"
                await ctx.channel.send(msg)
            elif fct == "update":
                msg = sql.updateField(ID, arg3, arg4, arg2)
                await ctx.channel.send(msg)
            elif fct == "value":
                msg = sql.valueAt(ID, arg3, arg2)
                await ctx.channel.send(msg)
            elif fct == "add":
                msg = sql.add(ID, arg3, arg4, arg2)
                await ctx.channel.send(msg)
            elif fct == "taille":
                msg = sql.taille(arg2)
                await ctx.channel.send(msg)
            else:
                await ctx.channel.send(":regional_indicator_s::regional_indicator_q::regional_indicator_l:")
        else:
            await ctx.channel.send("Tu n'est pas autorisé a utilisé cette commande!")

    @commands.command(pass_context=True)
    async def revive(self, ctx):
        await ctx.channel.send("Comme un phénix, <@604776153458278415> renait de ses cendres")


def setup(bot):
    bot.add_cog(Utils(bot))
    bot.add_cog(UtilsSecret(bot))
    open("help/cogs.txt", "a").write("Utils\n")
