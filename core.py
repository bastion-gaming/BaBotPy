import discord
from discord.ext import commands
from discord.ext.commands import Bot
from discord.utils import get
import sqlite3
import datetime as t
import DB
import roles
import stats as stat

# initialisation des variables.
DEFAUT_PREFIX = "!"

VERSION = open("fichier_txt/version.txt").read().replace("\n","")
TOKEN = open("fichier_txt/token.txt", "r").read().replace("\n","")
PREFIX = open("fichier_txt/prefix.txt","r").read().replace("\n","")
client = commands.Bot(command_prefix = "{0}".format(PREFIX))
NONE = open("fichier_txt/cogs.txt","w")
NONE = open("fichier_txt/help.txt","w")

client.remove_command("help")

# Au démarrage du Bot.
@client.event
async def on_ready():
	print('Connecté avec le nom : {0.user}'.format(client))
	print('PREFIX = '+str(PREFIX))
	print('\nBastionBot '+VERSION)
	print('| Core Module | >> Connecté !')

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

####################### Stat ####################################

@client.event
async def on_message(message):
	await stat.countMsg(message)
	await client.process_commands(message)

client.load_extension('stats')

####################### Commande roles.py #######################

client.load_extension('roles')

###################### Commande gestion.py #####################

client.load_extension('gestion')

####################### Commande gems.py #######################

client.load_extension('gems')

####################### Commande help.py #######################

client.load_extension('help')

client.run(TOKEN)
