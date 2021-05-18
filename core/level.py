from DB import SQLite as sql
from core import roles
from discord.ext import commands
from discord.ext.commands import bot
import discord
from core import welcome as wel
from core import gestion as ge
import datetime as dt


client = discord.Client()


def addxp(ID, nb, nameDB = None):
    if nameDB == None:
        nameDB = "bastion"
    balXP = sql.valueAtNumber(ID, "xp", nameDB)
    ns = balXP + int(nb)
    if ns <= 0:
        ns = 0
    sql.updateField(ID, "xp", ns, nameDB)


def lvlPalier(lvl):
    if lvl <= 0:
        return 10
    elif lvl == 1:
        return 30
    else:
        return int(100 * (2.5)**(lvl-2))


# BaBot | vérification du level
async def checklevel(message, nameDB = None):
    ID = message.author.id
    Nom = message.author.name
    member = message.guild.get_member(ID)
    if nameDB == None:
        nameDB = "bastion"
    try:
        lvl = sql.valueAtNumber(ID, "lvl", nameDB)
        xp = sql.valueAtNumber(ID, "xp", nameDB)
        palier = lvlPalier(lvl)
        if xp >= palier:
            sql.updateField(ID, "lvl", lvl+1, nameDB)
            desc = ":tada: {1} a atteint le niveau **{0}**".format(lvl+1, Nom)
            title = "Level UP"
            msg = discord.Embed(title = title, color= 6466585, description = desc)
            msg.set_thumbnail(url=message.author.avatar_url)
            await message.channel.send(embed = msg)

        lvl2 = sql.valueAtNumber(ID, "lvl", nameDB)
        if lvl == 0 and lvl2 == 1:
            await roles.addrole(member, "Joueurs")
            await roles.removerole(member, "Nouveau")
        return True
    except:
        return print("Le joueur n'existe pas.")


async def checklevelvocal(member):
    ID = member.id
    Nom = member.name
    nameDB = "bastion"
    channel_vocal = member.guild.get_channel(507679074362064916)
    try:
        lvl = sql.valueAtNumber(ID, "lvl", nameDB)
        lvl = int(lvl)
        xp = sql.valueAtNumber(ID, "xp", nameDB)
        xp = int(xp)
        palier = lvlPalier(lvl)
        if xp >= palier:
            sql.updateField(ID, "lvl", lvl+1, nameDB)
            desc = ":tada: {1} a atteint le niveau **{0}**".format(lvl+1, Nom)
            title = "Level UP"
            msg = discord.Embed(title = title, color= 6466585, description = desc)
            msg.set_thumbnail(url=member.avatar_url)
            await channel_vocal.send(embed = msg)
        lvl2 = sql.valueAtNumber(ID, "lvl", nameDB)
        if lvl == 0 and lvl2 == 1:
            await roles.addrole(member, "Joueurs")
            await roles.removerole(member, "Nouveau")
        return True
    except:
        return print("Le joueur n'existe pas.")


class Level(commands.Cog):

    def __init__(self, ctx):
        return(None)

    @commands.command(pass_context=True, aliases=['infos', 'inf'])
    async def info(self, ctx, Nom = None):
            """
            Permet d'avoir le level d'un utilisateur
            """
            if Nom == None:
                ID = ctx.author.id
                Nom = ctx.author.name
            elif len(Nom) == 21 :
                ID = int(Nom[2:20])
            elif len(Nom) == 22 :
                ID = int(Nom[3:21])
            else :
                msg = "Le nom que vous m'avez donné n'existe pas !"
                ID = -1
                await ctx.channel.send(msg)
                return

            if (ID != -1):
                if not ge.checkInfo(ID):
                    member = ctx.guild.get_member(int(ID))
                    await roles.addrole(member, "Nouveau")
                lvl = sql.valueAtNumber(ID, "lvl", "bastion")
                xp = sql.valueAtNumber(ID, "xp", "bastion")
                msg = "**Utilisateur:** {}".format(Nom)
                emb = discord.Embed(title = "Informations", color= 13752280, description = msg)

                if ctx.guild.id == wel.idBASTION:
                    # Niveaux part
                    msg = ""
                    palier = lvlPalier(lvl)
                    msg += "XP: `{0}/{1}`".format(xp, palier)
                    emb.add_field(name="**_Niveau_ : {0}**".format(lvl), value=msg, inline=False)

                    # Parrainage
                    P = sql.valueAt(ID, "parrain", "bastion")
                    F_li = sql.listFilleul(ID)
                    msg = ""
                    if P[0] != 0:
                        msg += "\nParrain: <@{0}>".format(P[0])
                    else :
                        msg += "\nParain: `None`"

                    if F_li != 0:
                        if int(sql.countFilleul(ID)) > 1:
                            sV = "s"
                        else:
                            sV = ""
                        msg += "\nFilleul{1} `x{0}`:".format(sql.countFilleul(ID), sV)
                        for one in F_li:
                            msg += "\n<@{}>".format(one[0])

                    emb.add_field(name="**_Parrainage_**", value=msg, inline=False)

                    await ctx.channel.send(embed = emb)
                else:
                    await ctx.channel.send("Commande utilisable uniquement sur le discord Bastion!")


def setup(bot):
    bot.add_cog(Level(bot))
    open("help/cogs.txt", "a").write("Level\n")
