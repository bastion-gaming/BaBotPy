import discord
import sqlite3
import welcome as wel
import roles
import datetime as t
import DB
from discord.ext import commands
from discord.ext.commands import Bot
from discord.utils import get
import gems

# initialisation des variables.
DEFAUT_PREFIX = "!"

VERSION = open("version.txt").read().replace("\n","")
TOKEN = open("token", "r").read().replace("\n","")

client = discord.Client()
PREFIX = open("prefix.txt","r").read().replace('\n','')

# Au démarrage du bot.
@client.event
async def on_ready():
    print('Connecté avec le nom : {0.user}'.format(client))
    print('PREFIX = '+str(PREFIX))
    print('BastionBot '+VERSION+' | Core Module | >> Connecté !')
    await wel.on_ready()
    await roles.on_ready()
    await gems.on_ready()
    DB.dbExist()

@client.event
async def on_member_join(member):
    await roles.autorole(member)
    channel = client.get_channel(478003352551030798)
    time = t.time()
    #data = sqlite3.connect('connect.db')
    #c = data.cursor()
    id = member.id
    if DB.newPlayer(id) == 100:
        await channel.send(f""":black_small_square:Bienvenue {member.mention} sur Bastion!:black_small_square: \n\n\nNous sommes ravis que tu aies rejoint notre communauté !\nTu es attendu :\n\n:arrow_right: Sur #⌈:closed_book:⌋•règles\n:arrow_right: Sur #⌈:ledger:⌋•liste-salons\n\n=====================""")
    else:
        await channel.send(f"""=====================\nBon retour parmis nous ! {member.mention}\n\n=====================""")
    #c.execute("""SELECT name FROM users WHERE id = ?""", (id,))
    #if c.fetchone() == None:
        # si le l'id est inconnue c'est une nouvelle personne qui se connecte !
    #    c.execute(""" INSERT INTO users VALUES(?,?,?) """, (id,member.mention, time))
    #    c.execute("""UPDATE compte SET nombre = nombre +1 WHERE ID = total""") #incrémente de 1 à chaque nouvelle personne
    #    data.commit()
    #    data.close()
    #    print(f'======\nAjout de {member.mention} à la BDD')
    #else :
        # si le nom est déjà dans la BDD on ne le recompte pas une deuxième fois
    #    await channel.send(f"""Ravis de te revoir parmis nous {member.mention} !!""")


@client.event
async def on_member_remove(member):
    channel = client.get_channel(478003352551030798)
    await channel.send(f"""{member.mention} nous a quitté, pourtant si jeune...""")


#Quand il y'a un message
@client.event
async def on_message(message):

    await gems.client.process_commands(message)
 ###################### Commande gems.py #######################

gems_client = commands.Bot(command_prefix = "{0}".format(PREFIX))

    DB.newPlayer(message.author.id)
    meco = message.content

    if meco.startswith(PREFIX+"create game"):
        meco2 = meco.replace(PREFIX+"create game ", "")
        await roles.create(message, meco2)

 ###################### Commande gems.py #######################

gems_client = commands.Bot(command_prefix = "{0}".format(prefix))

@gems_client.command(pass_context=True)
async def crime(ctx):
	await gems.crime(ctx)

@gems_client.command(pass_context=True)
async def bal(ctx):
    await gems.bal(ctx)

@gems_client.command(pass_context=True)
async def inv(ctx):
    await gems.inv(ctx)

@gems_client.command(pass_context=True)
async def mine(ctx):
    await gems.mine(ctx)

@gems_client.command(pass_context=True)
async def begin(ctx):
    await gems.begin(ctx)

@gems_client.command(pass_context=True)
async def gamble(ctx):
    await gems.gamble(ctx,mise)

@gems_client.command(pass_context=True)
async def buy(ctx):
    await gems.buy(ctx,item,nombre)

@gems_client.command(pass_context=True)
async def sell(ctx):
    await gems.sell(ctx,item,nombre)

@gems_client.command(pass_context=True)
async def pay(ctx):
    await gems.pay(ctx,nom,don)

###################### Commande gems.py #######################
gems_client.run(TOKEN)

client.run(TOKEN)
