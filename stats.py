import random as r
import datetime as dt
import DB
from discord.ext import commands, tasks
from discord.ext.commands import bot
from discord.utils import get
import discord
import json

client = discord.Client()
file = "time.json"


def fileExist():
    try:
        with open(file):
            pass
    except IOError:
        return False
    return True


async def countMsg(message):
    id = message.author.id
    DB.updateField(id, "nbMsg", int(DB.valueAt(id, "nbMsg") + 1))
    return DB.valueAt(id, "nbMsg")


def countTotalMsg():
    # Init a
    a = 0
    for item in DB.db:
        # On additionne le nombre de message posté en tout
        a = a + int(item["nbMsg"])
    return a


def hourCount():
    d = dt.datetime.now().hour
    if fileExist() == False:
        t = {
            "0": 0,
            "1": 0,
            "2": 0,
            "3": 0,
            "4": 0,
            "5": 0,
            "6": 0,
            "7": 0,
            "8": 0,
            "9": 0,
            "10": 0,
            "11": 0,
            "12": 0,
            "13": 0,
            "14": 0,
            "15": 0,
            "16": 0,
            "17": 0,
            "18": 0,
            "19": 0,
            "20": 0,
            "21": 0,
            "22": 0,
            "23": 0,
        }
        t[str(d)] = int(countTotalMsg())
        with open(file, "w") as f:
            f.write(json.dumps(t, indent=4))
        return d
    else:
        with open(file, "r") as f:
            t = json.load(f)
            t[str(d)] = int(countTotalMsg())
        with open(file, "w") as f:
            f.write(json.dumps(t, indent=4))
    print("time.json modifié")


# ===============================================================


class Stats(commands.Cog):
    def __init__(self, ctx):
        self.hourWrite.start()
        return None

    def cog_unload(self):
        self.hourWrite.cancel()

    @tasks.loop(hours=1.0)
    async def hourWrite(self):
        """
		Va, toute les heures, écrire dans time.json le nombre total de message écrit sur le serveur.
		"""
        hourCount()

    @commands.command(pass_context=True)
    async def totalMsg(self, ctx):
        """
		Permet de savoir combien i y'a eu de message posté depuis que le bot est sur le serveur
		"""
        msg = (
            "Depuis que je suis sur ce serveur il y'a eu : "
            + str(countTotalMsg())
            + " messages."
        )
        await ctx.channel.send(msg)

    @commands.command(pass_context=True)
    async def hourMsg(self, ctx, ha=None, hb=None):
        """
		Permet de savoir combien i y'a eu de message posté dans l'heure ou entre deux heures.
		"""
        d = dt.datetime.now().hour
        if fileExist() == False:
            nbMsg = totalMsg()
            await ctx.channel.send(
                "le fichier time.json est introuvable le résultat sera donc peut être faux."
            )
        else:
            hourCount()
            with open(file, "r") as f:
                t = json.load(f)
            if ha != None and hb != None:
                ha = int(ha)
                hb = int(hb)
                if ha >= 0 and hb >= 0 and ha < 24 and hb < 24:
                    nbMsg = t[str(hb)] - t[str(ha)]
                    msg = (
                        "Entre "
                        + str(ha)
                        + "h et "
                        + str(hb)
                        + "h il y a eu "
                        + str(nbMsg)
                        + " messages."
                    )
                else:
                    msg = "Vous avez entré une heure impossible."
            else:
                if d != 0:
                    nbMsg = t[str(d)] - t[str(d - 1)]
                else:
                    nbMsg = t["0"] - t["23"]
                msg = (
                    "Depuis "
                    + str(d)
                    + "h il y'a eu: "
                    + str(nbMsg)
                    + " messages postés."
                )
        await ctx.channel.send(msg)


def setup(bot):
    bot.add_cog(Stats(bot))
    open("fichier_txt/cogs.txt", "a").write("Stats\n")
