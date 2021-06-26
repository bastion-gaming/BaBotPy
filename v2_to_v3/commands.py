import requests
from discord.ext import commands
from discord.ext.commands import bot
import discord
from core import gestion as ge, level, welcome as we
from v2_to_v3 import SQLite as sql
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
                print(f"{i}/{taille}: Created")

            for i in range(1, taille+1):
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
                print(f"{i}/{taille}: {did}, {arr}, {nbm}, {nbr}, {lvl}, {xp}, {par}")
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


def setup(bot):
    bot.add_cog(CommandesOld(bot))
