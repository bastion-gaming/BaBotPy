import discord
from discord.ext import commands
from discord.ext.commands import bot


class Helpme(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    async def help(self, ctx):
        """Affiche ce message !"""
        d_help = "Liste de toutes les commandes utilisable"
        msg = discord.Embed(title = "Aide", color= 9576994, description = d_help)

        COGS = open("core/cache/cogs.txt", "r").read()
        COGS = COGS.split('\n')
        COGS.pop()

        for COG in COGS:
            desc = ""
            desctemp = ""
            cog = self.bot.get_cog(COG)
            coms = cog.get_commands()
            for com in coms :
                desctemp += "`{0}` {1}\n".format(com.name, com.help)
                if len(desctemp) < 1000:
                    desc += "`{0}` {1}\n".format(com.name, com.help)
                else:
                    msg.add_field(name=COG, value=desc, inline=False)
                    desctemp = "`{0}` {1}\n".format(com.name, com.help)
                    desc = "`{0}` {1}\n".format(com.name, com.help)
            msg.add_field(name=COG, value=desc, inline=False)
        # await bot.delete_message(ctx.message)
        await ctx.send(embed = msg, delete_after = 120)


def setup(bot):
    bot.add_cog(Helpme(bot))
