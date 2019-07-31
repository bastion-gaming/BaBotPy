import discord
import random as r
import time as t
import DB
from discord.ext import commands
from discord.ext.commands import Bot
from discord.utils import get

message_crime = ["You robbed the Society of Schmoogaloo and ended up in a lake,but still managed to steal ",
"tu as volé une pomme qui vaut ", "tu as gangé le loto ! prends tes ", "j'ai plus d'idée prends ça "]
# 4 phrases
message_gamble = ["tu as remporté le pari ! tu obtiens ","Une grande victoire pour toi ! tu gagnes ",
"bravo prends ", "heu.... "]
# 4 phrases
# se sont les phrases prononcé par le bot pour plus de diversité
couldown_xl = 16
couldown_l = 8 # l pour long
couldown_c = 4 # c pour court
# nb de sec nécessaire entre 2 commandes
PREFIX = open("prefix.txt","r").read().replace('\n','')

client = commands.Bot(command_prefix = "{0}".format(PREFIX))

@client.event  # event decorator/wrapper. More on decorators here: https://pythonprogramming.net/decorators-intermediate-python-tutorial/
async def on_ready():  # method expected by client. This runs once when connected
    print(f'BastionBot | Gems Module | >> Connecté !')  # notification of login.

def spam(ID,couldown):
	time = DB.valueAt(ID, "com_time")
	# on récupère le la date de la dernière commande
	return(time < t.time()-couldown)

def addGems(ID, nbGems):
    """
    Permet d'ajouter un nombre de gems à quelqu'un. Il nous faut son ID et le nombre de gems.
    Si vous souhaitez en retirer mettez un nombre négatif.
    """
    old_value = DB.valueAt(ID, "gems")
    new_value = old_value + nbGems
    DB.updateField(ID, "gems", "new_value")
    print("Le compte de "+str(ID)+ " est maintenant de: "+str(new_value))

    return new_value

@client.command(pass_context=True)
async def crime(ctx):
    """commets un crime et gagne des gems !"""
    ID = ctx.message.author.id
    if spam(ID,couldown_l):
        # si 10 sec c'est écoulé depuis alors on peut en  faire une nouvelle
        gain = r.randint(5,10)
        msg = message_crime[r.randint(0,3)]+str(gain)+":gem:"
        addGems(ID, gain)
        DB.updateField(ID, "com_time", t.time())
    else:
        msg = "il faut attendre "+str(couldown_l)+" secondes entre chaque commande !"

    await ctx.message.channel.send(msg)

@client.command(pass_context=True)
async def bal(ctx):
    """êtes vous riche ou pauvre ? bal vous le dit """
    ID = ctx.message.author.id
    if spam(ID,couldown_c):
        DB.updateField(ID, "com_time", t.time())
        gem = DB.valueAt(ID, "gems")
        msg = "tu as actuellement : "+str(gem)+" :gem: !"
    else:
        msg = "il faut attendre "+str(couldown_c)+" secondes entre chaque commande !"
    await ctx.message.channel.send(msg)
