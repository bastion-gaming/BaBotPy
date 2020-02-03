import discord
from discord.ext import commands
from discord.ext.commands import bot
from discord.utils import get


class Helpme(commands.Cog):

    def __init__(self, bot):
        self.PREFIX = open("core/prefix.txt", "r").read().replace("\n", "")
        self.bot = bot

    @commands.command(pass_context=True)
    async def help(self, ctx, nameElem = None):
        """Affiche ce message !"""
        d_help = "Liste de toutes les fonctions utilisable avec le prefix {}".format(self.PREFIX)
        msg = discord.Embed(title = "Fonction disponible", color= 9576994, description = d_help)
        arg = ""

        COGS = open("help/cogs.txt", "r").read()
        COGS = COGS.split('\n')
        COGS.pop()

        if nameElem != None:
            nameElem = nameElem.lower()
            if nameElem == "gems":
                for COG in COGS:
                    mCOG = COG.lower()
                    if mCOG == "gems" or mCOG == "gemsbase" or mCOG == "gemsplay" or mCOG == "gemsevent" or mCOG == "gemsfight" or mCOG == "gemsguild":
                        cog = self.bot.get_cog(COG)
                        coms = cog.get_commands()
                        for com in coms :
                            arg += "• "+str(com.name)+" : "+str(com.help)+"\n"
                        msg.add_field(name=COG, value=arg, inline=False)
                        arg = ""
                await ctx.send(embed = msg, delete_after = 60)
                return
            else:
                for COG in COGS:
                    mCOG = COG.lower()
                    if nameElem == "img":
                        nameElem = "images"
                    if mCOG == nameElem:
                        cog = self.bot.get_cog(COG)
                        coms = cog.get_commands()
                        for com in coms :
                            arg += "• "+str(com.name)+" : "+str(com.help)+"\n"
                        msg.add_field(name=COG, value=arg, inline=False)
                        await ctx.send(embed = msg, delete_after = 60)
                        return
        else:
            msg.add_field(name="GitHub", value="https://github.com/bastion-gaming/bot-discord/blob/master/help/Help.md", inline=False)
            for COG in COGS:
                cog = self.bot.get_cog(COG)
                coms = cog.get_commands()
                arg += "\n• "+str(COG)
            msg.add_field(name="Liste des modules", value=arg, inline=False)
            await ctx.send(embed = msg, delete_after = 60)


def setup(bot):
    bot.add_cog(Helpme(bot))
