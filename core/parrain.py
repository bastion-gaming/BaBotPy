from DB import SQLite as sql
from discord.ext import commands
from discord.ext.commands import bot
import discord
from core import welcome as wel, level as lvl

client = discord.Client()


# ===============================================================
class Parrain(commands.Cog):

    def __init__(self, bot):
        return (None)

    @commands.command(pass_context=True)
    async def parrain(self, ctx, nom=None):
        """
        Permet d'ajouter un joueur comme parrain.
        En le faisant vous touchez un bonus et lui aussi
        """
        if ctx.guild.id == wel.idBASTION:
            ID = ctx.author.id
            if nom != None :
                ID_p = sql.nom_ID(nom)
                print(ID_p)
                print(sql.get_PlayerID(ID_p, "bastion"))
                print(sql.valueAt(ID, "parrain", "bastion"))
                if sql.get_PlayerID(ID_p, "bastion") != "Error 404" and sql.valueAtNumber(ID, "parrain", "bastion") == 0 and ID_p != ID:
                    sql.updateField(ID, "parrain", ID_p, "bastion")
                    # print("Parrain ajouté")
                    sql.add(ID_p, ID, 1, "filleuls")
                    lvl.addxp(ID, 15)
                    fil_L = sql.countFilleul(ID_p)
                    gain_p = 100 * int(fil_L)
                    lvl.addxp(ID_p, gain_p)
                    msg = "Votre parrain a bien été ajouté ! Vous empochez 15 XP et lui {0} XP.".format(gain_p)
                else :
                    # print("Impossible d'ajouter ce joueur comme parrain")
                    msg = "Impossible d'ajouter ce joueur comme parrain"

            await ctx.channel.send(msg)
        else:
            await ctx.channel.send("commande utilisable uniquement sur le discord `Bastion`")

    @commands.command(pass_context=True)
    async def filleul(self, ctx, nom = None):
        """
        Affiche la liste des filleuls d'un joueur
        """
        if ctx.guild.id == wel.idBASTION or True:
            if nom == None:
                ID = ctx.author.id
                nom = ctx.author.name
            else :
                ID = sql.nom_ID(nom)
                if ID == -1:
                    msg = "Ce joueur n'existe pas !"
                    await ctx.channel.send(msg)
                    return

            F_li = sql.listFilleul(ID)
            if F_li != 0:
                if int(sql.countFilleul(ID)) > 1:
                    sV = "s"
                else:
                    sV = ""
                msg = "Filleul{1} `x{0}`:".format(sql.countFilleul(ID), sV)
                for one in F_li:
                    msg += "\n<@{}>".format(one[0])
                emb = discord.Embed(title = "Informations :", color= 13752280, description = msg)
                await ctx.channel.send(embed = emb)
            else:
                msg = "Vous n'avez pas de filleul, invitez de nouveaux joueurs !"
                await ctx.channel.send(msg)
        else:
            await ctx.channel.send("commande utilisable uniquement sur le discord `Bastion`")

    @commands.command(pass_context=True)
    async def filleul_supp(self, ctx, nom):
        """
        Affiche la liste des filleuls d'un joueur
        """
        if ctx.guild.id == wel.idBASTION or True:
            ID_p = ctx.author.id
            ID_f = sql.nom_ID(nom)
            if ID_f == -1:
                msg = "Ce joueur n'existe pas !"
                await ctx.channel.send(msg)
                return

            parrain = sql.valueAt(ID_f, "parrain", "bastion")
            if parrain == 0:
                return await ctx.channel.send("Ce joueur n'a pas de parrain")
            if parrain[0] == ID_p:
                sql.updateField(ID_f, "parrain", "", "bastion")
                lvl.addxp(ID_f, -15)
                fil_count = sql.countFilleul(ID_p)
                gain_p = -100 * int(fil_count)
                lvl.addxp(ID_p, gain_p)
                msg = "Votre filleul <@{filleul}> a bien été retiré ! Vous perdez {xp_p} XP et lui 15 XP.".format(filleul=ID_f, xp_p=gain_p)
            else:
                msg = "Vous n'etes pas son parrain !"
            await ctx.channel.send(msg)
        else:
            await ctx.channel.send("commande utilisable uniquement sur le discord `Bastion`")


def setup(bot):
    bot.add_cog(Parrain(bot))
    open("help/cogs.txt", "a").write("Parrain\n")
