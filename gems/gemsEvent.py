import discord
from gems import gemsFonctions as GF
from discord.ext import commands
from discord.ext.commands import bot


class GemsEvent(commands.Cog):

    def __init__(self, ctx):
        return(None)

    @commands.command(pass_context=True)
    async def event(self, ctx):
        """Date des Événements !!"""
        msg = discord.Embed(title = "Evénements", color= 13752280, description = "Date des Evénements !!")
        desc = "26 Octobre :arrow_right: 10 Novembre"
        desc += "\n<:gem_pumpkin:{0}>`pumpkin`".format(GF.get_idmoji("pumpkin"))
        desc += "\n<:gem_pumpkinpie:{0}>`pumpkinpie`".format(GF.get_idmoji("pumpkinpie"))
        msg.add_field(name="Halloween", value=desc, inline=False)

        desc = "21 Décembre :arrow_right: 14 Janvier"
        desc += "\n<:gem_cupcake:{0}>`cupcake`".format(GF.get_idmoji("cupcake"))
        desc += "\n:gift:`gift`"
        msg.add_field(name="Noël", value=desc, inline=False)
        await ctx.channel.send(embed = msg)


def setup(bot):
    bot.add_cog(GemsEvent(bot))
    open("help/cogs.txt", "a").write("GemsEvent\n")
