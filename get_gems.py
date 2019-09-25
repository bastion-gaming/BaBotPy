import discord
from discord.ext import commands, tasks
from discord.ext.commands import Bot
from discord.utils import get

import DB

# initialisation des variables.
DEFAUT_PREFIX = "*"

idGetGems = 620558080551157770
idBASTION = 417445502641111051

VERSION = open("fichier_txt/version.txt").read().replace("\n","")
TOKEN = open("fichier_txt/token_getgems.txt", "r").read().replace("\n","")
client = commands.Bot(command_prefix = "{0}".format(DEFAUT_PREFIX))
NONE = open("fichier_txt/cogs.txt","w")
NONE = open("fichier_txt/help.txt","w")

client.remove_command("help")

# Au démarrage du Bot.
@client.event
async def on_ready():
	print('Connecté avec le nom : {0.user}'.format(client))
	print('PREFIX = '+str(DEFAUT_PREFIX))
	print('\nBastionBot '+VERSION)
	print('------\n')


@client.event
async def on_member_remove(member):
	ID = member.id
	if member.guild.id != idBASTION:
		gems = DB.valueAt(ID, "gems")
		BotGems = DB.valueAt(idGetGems, "gems")
		pourcentage = 0.02
		transfert = gems * pourcentage
		DB.updateField(idGetGems, "gems", BotGems + int(transfert))
		DB.updateField(ID, "gems", gems - int(transfert))


####################### Commande help.py #######################

client.load_extension('help')

################### Core ############################

client.load_extension('utils')

####################### Commande gems.py #######################

client.load_extension('gems')

####################### Lancemement du bot ######################


client.run(TOKEN)
