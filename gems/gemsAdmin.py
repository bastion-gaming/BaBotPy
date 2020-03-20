import discord
from discord.ext import commands
from discord.ext.commands import bot
from gems import gemsFonctions as GF
from core import gestion as ge
import gg_lib as gg


class GemsAdmin(commands.Cog):

    def __init__(self, ctx):
        return(None)

    @commands.command(pass_context=True)
    async def admin(self, ctx, fct = None, ID = None, arg2 = None, arg3 = None, arg4 = None):
        if ID == None:
            ID = ctx.author.id
        else:
            try:
                ID = int(ID)
            except:
                ID = ge.nom_ID(ID)
        param = dict()
        param["ID"] = ID
        param["fct"] = fct
        param["arg2"] = arg2
        param["arg3"] = arg3
        param["arg4"] = arg4
        if ge.permission(ctx, ge.admin):
            ge.socket.send_string(gg.std_send_command("admin", ID, ge.name_pl, param))
            msg = GF.msg_recv()
            await ctx.channel.send(msg[1])
        else:
            await ctx.channel.send("[Admin Command] Tu n'est pas autorisé à utiliser cette commande!")


def setup(bot):
    bot.add_cog(GemsAdmin(bot))
