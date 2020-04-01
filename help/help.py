import discord
from discord.ext import commands
from discord.ext.commands import bot

GGnom = ["gem", "gems", "gg", "getgems", "get gems"]

class Helpme(commands.Cog):

    def __init__(self, bot):
        self.PREFIX = open("core/prefix.txt", "r").read().replace("\n", "")
        self.bot = bot

    @commands.command(pass_context=True)
    async def help(self, ctx, nameElem = None):
        """Affiche ce message !"""
        d_help = "Liste de toutes les commandes utilisable avec le prefix {}".format(self.PREFIX)
        msg = discord.Embed(title = "Commandes disponible", color= 9576994, description = d_help)
        desc = ""
        desctemp = ""

        COGS = open("help/cogs.txt", "r").read()
        COGS = COGS.split('\n')
        COGS.pop()

        if nameElem != None:
            nameElem = nameElem.lower()
            if nameElem in GGnom:
                for COG in COGS:
                    mCOG = COG.lower()
                    if "gems" in mCOG:
                        cog = self.bot.get_cog(COG)
                        coms = cog.get_commands()
                        for com in coms :
                            desctemp += "• {0} : {1}\n".format(com.name, com.help)
                            if len(desctemp) < 1000:
                                desc += "• {0} : {1}\n".format(com.name, com.help)
                            else:
                                msg.add_field(name=COG, value=desc, inline=False)
                                desctemp = "• {0} : {1}\n".format(com.name, com.help)
                                desc = "• {0} : {1}\n".format(com.name, com.help)
                        msg.add_field(name=COG, value=desc, inline=False)
                        desc = ""
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
                            desctemp += "• {0} : {1}\n".format(com.name, com.help)
                            if len(desctemp) < 1000:
                                desc += "• {0} : {1}\n".format(com.name, com.help)
                            else:
                                msg.add_field(name=COG, value=desc, inline=False)
                                desctemp = "• {0} : {1}\n".format(com.name, com.help)
                                desc = "• {0} : {1}\n".format(com.name, com.help)
                        msg.add_field(name=COG, value=desc, inline=False)
                        await ctx.send(embed = msg, delete_after = 60)
                        return
        else:
            GGdesc = ""
            msg.add_field(name="GitHub", value="https://github.com/bastion-gaming/bot-discord/blob/master/help/Help.md", inline=False)
            for COG in COGS:
                if "gems" in COG.lower():
                    GGdesc += "\n• {0}".format(COG)
                else:
                    cog = self.bot.get_cog(COG)
                    coms = cog.get_commands()
                    desc += "\n• {0}".format(COG)
            msg.add_field(name="Modules BaBot", value=desc, inline=False)
            if GGdesc != "":
                msg.add_field(name="Modules Get Gems", value=GGdesc, inline=False)
            await ctx.send(embed = msg)


def setup(bot):
    bot.add_cog(Helpme(bot))
