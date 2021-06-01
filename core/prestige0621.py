from DB import SQLite as sql
from discord.ext import commands
from discord.ext.commands import bot
import discord
from operator import itemgetter

client = discord.Client()


# ===============================================================
class Prestige0621(commands.Cog):

    def __init__(self, bot):
        return (None)

    @commands.command(pass_context=True)
    async def prestige(self, ctx):
        if ctx.guild.id == wel.idBASTION:
            if ge.permission(ctx, ge.Inquisiteur):
                UserList = []
                taille = sql.taille("bastion")
                i = 1
                while i <= taille:
                    IDi = sql.userID(i, "bastion")
                    nbMsg = sql.valueAtNumber(IDi, "nbmsg", "bastion")
                    XP = sql.valueAtNumber(IDi, "xp", "bastion")
                    Arrival = sql.valueAtNumber(IDi, "arrival", "bastion")[:10]
                    try:
                        Name = ctx.guild.get_member(IDi).name
                        UserList.append([IDi, XP, nbMsg, Arrival, Name])
                        i += 1
                    except:
                        i += 1
                UserList = sorted(UserList, key=itemgetter(1), reverse=True)
                j = 1
                n = 10
                for one in UserList:
                    if j <= n:
                        ID = one[0]
                        XP = one[1]
                        lvl = sql.valueAtNumber(ID, "lvl", "bastion")
                        nbMsg = one[2]
                        nbReact = sql.valueAtNumber(ID, "nbreaction", "bastion")
                        sql.updateField(ID, "lvl_0621", int(lvl), "bastion")
                        sql.updateField(ID, "xp_0621", int(XP), "bastion")
                        sql.updateField(ID, "top_0621", int(j), "bastion")

                        sql.updateField(ID, "lvl", 1, "bastion")
                        XP = 10 + int(nbReact) + int(nbMsg)
                        sql.updateField(ID, "xp", XP, "bastion")
                    j += 1

                i = 1
                while i <= taille:
                    IDi = sql.userID(i, "bastion")
                    lvl = sql.valueAtNumber(ID, "lvl", "bastion")
                    if int(lvl) >= 1:
                        nbMsg = sql.valueAtNumber(IDi, "nbmsg", "bastion")
                        nbReact = sql.valueAtNumber(IDi, "nbreaction", "bastion")
                        sql.updateField(IDi, "lvl", 1, "bastion")
                        XP = 10 + int(nbReact) + int(nbMsg)
                        sql.updateField(IDi, "xp", XP, "bastion")
                    i += 1
                msg = "Prestige terminé"
                await ctx.channel.send(msg)
            else :
                await ctx.channel.send("Tu ne peux pas exécuter cette commande.")
        else:
            await ctx.channel.send("commande utilisable uniquement sur le discord `Bastion`")


def setup(bot):
    bot.add_cog(Prestige0621(bot))
