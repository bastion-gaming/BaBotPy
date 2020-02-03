from DB import TinyDB as DB, SQLite as sql
from discord.ext import commands, tasks
from discord.ext.commands import bot
from discord.utils import get
import discord
from core import welcome as wel

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
                    print("Parrain ajouté")
                    sql.add(ID_p, ID, 1, "filleuls")
                    sql.addGems(ID, 50)
                    fil_L = sql.valueAt(ID_p, "all", "filleuls")
                    gain_p = 100 * len(fil_L)
                    sql.addGems(ID_p, gain_p)
                    msg = "Votre parrain a bien été ajouté ! Vous empochez 50 :gem: et lui "+str(gain_p)+" :gem:."
                else :
                    print("Impossible d'ajouter ce joueur comme parrain")
                    msg = "Impossible d'ajouter ce joueur comme parrain"

            await ctx.channel.send(msg)
        else:
            await ctx.channel.send("commande utilisable uniquement sur le discord `Bastion`")

    @commands.command(pass_context=True)
    async def filleul(self, ctx, nom = None):
        """
        Affiche la liste des filleuls d'un joueur
        """
        if ctx.guild.id == wel.idBASTION:
            if nom == None:
                ID = ctx.author.id
                nom = ctx.author.name
            else :
                ID = sql.nom_ID(nom)
                if ID == -1:
                    msg = "Ce joueur n'existe pas !"
                    await ctx.channel.send(msg)
                    return

            F_li = sql.valueAt(ID, "all", "filleuls")
            if F_li != 0:
                if len(F_li) > 1:
                    sV = "s"
                else:
                    sV = ""
                msg = "Filleul{1} `x{0}`:".format(len(F_li), sV)
                for one in F_li:
                    msg += "\n<@{}>".format(one[0])
                emb = discord.Embed(title = "Informations :", color= 13752280, description = msg)
                await ctx.channel.send(embed = emb)
            else:
                msg = "Vous n'avez pas de filleul, invitez de nouveaux joueurs !"
                await ctx.channel.send(msg)
        else:
            await ctx.channel.send("commande utilisable uniquement sur le discord `Bastion`")


def setup(bot):
    bot.add_cog(Parrain(bot))
    open("help/cogs.txt", "a").write("Parrain\n")
