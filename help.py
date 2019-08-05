import discord
import random as r
import time as t
from discord.ext import commands
from discord.ext.commands import bot
from discord.utils import get

class Helpme(commands.Cog):

    def __init__(self,ctx):
        self.PREFIX = open("prefix.txt","r").read().replace("\n","")

    @commands.command(pass_context=True)
    async def help(self, ctx):
        d_help = "Liste de toutes les fonctions utilisable avec le prefix {}".format(self.PREFIX)
        d_Gems = "~crime : blablablabla blablabla blabla blabla\n~bal : blablablabla blablabla blabla blabla\n~pay :blablablabla blablabla blabla blabla"
        d_Gestion = "*commande reserver au inquisiteur*\n~supp <nb>: supprime x messages\n~show_perm: montre les roles de la personne"
        d_Role = "*commande reserver au inquisiteur*\n~creategame <nom> <categori> : créé un jeux "
        msg = discord.Embed(title = "Fonction disponible",color= 12745742, description = d_help)
        msg.add_field(name="Gems", value=d_Gems, inline=False)
        msg.add_field(name="Gestion", value=d_Gestion, inline=False)
        msg.add_field(name="Role", value=d_Role, inline=False)
        await ctx.channel.send(embed = msg)


def setup(bot):
	bot.add_cog(Helpme(bot))
