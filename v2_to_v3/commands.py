import requests
from discord.ext import commands
from discord.ext.commands import bot
import discord
from core import gestion as ge, level, welcome as we
from core import SQLite as sql
import datetime as dt


class CommandesOld(commands.Cog):

    def __init__(self, ctx):
        return(None)

    @commands.command(pass_context=True)
    async def tdb(self, ctx):
        """Transfert DB v2 vers v3"""
        if ge.permission(ctx, ge.Inquisiteur):
            taille = sql.taille()
            for i in range(1, taille+1):
                did = sql.userID(i)
                req = requests.get('http://{ip}/users/playerid/{discord_id}'.format(ip=ge.API_IP, discord_id=did)).json()
                if req['error'] == 404:
                    r = requests.post('http://{ip}/users/create/?discord_id={discord_id}'.format(ip=ge.API_IP, discord_id=did))
                print(f"{i} OK")

            for i in range(165, taille+1):
                did = sql.userID(i)
                arr = sql.valueAtNumber(did, "arrival")
                if arr == "0":
                    arr = str(dt.date.today())
                arr = arr[:10]
                nbm = sql.valueAtNumber(did, "nbmsg")
                nbr = sql.valueAtNumber(did, "nbreaction")
                if nbr is None:
                    nbr = 0
                lvl = sql.valueAtNumber(did, "lvl")
                xp = sql.valueAtNumber(did, "xp")
                par = sql.valueAtNumber(did, "parrain")
                print(f"{did}, {arr}, {nbm}, {nbr}, {lvl}, {xp}, {par}")
                req = requests.get('http://{ip}/users/playerid/{discord_id}'.format(ip=ge.API_IP, discord_id=did)).json()
                r = requests.put('http://{ip}/old/{PlayerID}/{arrival}/{niv}/{xp}/{nbmsg}/{nbreaction}/{parrain}'.format(
                    ip=ge.API_IP,
                    PlayerID=req['ID'],
                    arrival=arr,
                    niv=lvl,
                    xp=xp,
                    nbmsg=nbm,
                    nbreaction=nbr,
                    parrain=par
                ))
            desc = "Transfert terminé"
        else :
            desc = "Tu ne remplis pas les conditions, tu fais partie de la plèbe !"
        msg = discord.Embed(title = "Message de Babot", color= 9576994, description = desc)
        await ctx.send(embed = msg, delete_after = 20)

    @commands.command(pass_context=True)
    async def infox(self, ctx, Nom = None):
        """
        Permet d'avoir les informations d'un utilisateur
        """
        if Nom == None:
            ID = ctx.author.id
            Nom = ctx.author.name
        else:
            ID = ge.nom_ID(Nom)

        if ID != -1:
            if not level.checkInfo(ID):
                member = ctx.guild.get_member(int(ID))
                await ge.addrole(member, "Nouveau")
            PlayerID = requests.get('http://{ip}/users/playerid/{discord_id}'.format(ip=ge.API_IP, discord_id=ID)).json()['ID']
            user = requests.get('http://{ip}/users/{player_id}'.format(ip=ge.API_IP, player_id=PlayerID)).json()
            lvl = int(user['level'])
            xp = int(user['xp'])
            nbmsg = int(user['nbmsg'])
            reaction = int(user['nbreaction'])
            msg = "**Utilisateur:** {}".format(Nom)
            emb = discord.Embed(title = "Informations", color= 13752280, description = msg)

            if ctx.guild.id == wel.idBASTION:
                # Niveaux part
                msg = ""
                palier = level.lvlPalier(lvl)
                msg += "XP: `{0}/{1}`\n".format(xp, palier)
                msg += "Messages: `{0}`\n".format(nbmsg)
                msg += "Réactions: `{0}`\n".format(reaction)
                emb.add_field(name="**_Niveau_ : {0}**".format(lvl), value=msg, inline=False)

                # Parrainage
                P = user['godparent']
                F_li = requests.get('http://{ip}/users/godchilds/{player_id}'.format(ip=ge.API_IP, player_id=PlayerID)).json()
                nbF = int(requests.get('http://{ip}/users/godchilds/count/{player_id}'.format(ip=ge.API_IP, player_id=PlayerID)).text)
                msg = ""
                if P != 0:
                    msg += "\nParrain: <@{0}>".format(requests.get('http://{ip}/users/{player_id}'.format(ip=ge.API_IP, player_id=P)).json()['discord_id'])
                else :
                    msg += "\nParain: `None`"

                if nbF != 0:
                    if nbF > 1:
                        sV = "s"
                    else:
                        sV = ""
                    msg += "\nFilleul{1} `x{0}`:".format(nbF, sV)
                    for one in F_li:
                        msg += "\n<@{}>".format(one[0])

                emb.add_field(name="**_Parrainage_**", value=msg, inline=False)

                await ctx.channel.send(embed = emb)
            else:
                await ctx.channel.send("Commande utilisable uniquement sur le discord Bastion!")
        else:
            msg = "Le nom que vous m'avez donné n'existe pas !"
            await ctx.channel.send(msg)


def setup(bot):
    bot.add_cog(CommandesOld(bot))
