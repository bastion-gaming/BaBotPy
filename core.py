import discord
from discord.ext import commands
from discord.ext.commands import Bot
from discord.utils import get
import sqlite3
import datetime as t
#import welcome as wel
import roles
import DB
import gems
import gestion as ges

# initialisation des variables.
DEFAUT_PREFIX = "!"

VERSION = open("version.txt").read().replace("\n","")
TOKEN = open("token", "r").read().replace("\n","")
PREFIX = open("prefix.txt","r").read().replace("\n","")
client = commands.Bot(command_prefix = "{0}".format(PREFIX))

# Au démarrage du bot.
@client.event
async def on_ready():
    print('Connecté avec le nom : {0.user}'.format(client))
    print('PREFIX = '+str(PREFIX))
    print('\nBastionBot '+VERSION)
    print('| Core Module | >> Connecté !')
    await roles.on_ready()
    await gems.on_ready()

@client.event
async def on_member_join(member):
    await roles.autorole(member)
    channel = client.get_channel(417445503110742048)
    time = t.time()
    #data = sqlite3.connect('connect.db')
    #c = data.cursor()
    id = member.id
    if DB.newPlayer(id) == 100:
        msg = ":black_small_square:Bienvenue {} sur Bastion!:black_small_square: \n\n\nNous sommes ravis que tu aies rejoint notre communauté !\nTu es attendu :\n\n:arrow_right: Sur #⌈:closed_book:⌋•règles\n:arrow_right: Sur #⌈:ledger:⌋•liste-salons\n\n=====================".format(member.mention)
    else:
        msg = "=====================\nBon retour parmis nous ! {}\n\n=====================".format(member.mention)
    await channel.send(msg)

@client.event
async def on_member_remove(member):
    channel = client.get_channel(417445503110742048)
    await channel.send("{member.mention} nous a quitté, pourtant si jeune...")

####################### Commande roles.py #######################

@client.command(pass_context=True)
async def creategame(ctx, game, categorie):
    await roles.creategame(ctx, game, categorie)

###################### Commande roles.py #######################

###################### Commande gestion.py #####################

@client.command(pass_context=True)
async def supp(ctx,nb):
    await ges.supp(ctx,nb)

###################### Commande gestion.py #####################

####################### Commande gems.py #######################

@client.command(pass_context=True)
async def crime(ctx):
    await gems.crime(ctx)

@client.command(pass_context=True)
async def bal(ctx):
    await gems.bal(ctx)

@client.command(pass_context=True)
async def inv(ctx):
    await gems.inv(ctx)

@client.command(pass_context=True)
async def mine(ctx):
    await gems.mine(ctx)

@client.command(pass_context=True)
async def begin(ctx):
    await gems.begin(ctx)

@client.command(pass_context=True)
async def gamble(ctx,mise):
    await gems.gamble(ctx,mise)

@client.command(pass_context=True)
async def buy(ctx,item,nombre):
    await gems.buy(ctx,item,nombre)

@client.command(pass_context=True)
async def sell(ctx,item,nombre):
    await gems.sell(ctx,item,nombre)

@client.command(pass_context=True)
async def pay(ctx,nom,don):
    await gems.pay(ctx,nom,don)
####################### Commande gems.py #######################

client.run(TOKEN)
