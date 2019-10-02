import discord
from discord.ext import commands, tasks
from discord.ext.commands import Bot
from discord.utils import get

from DB import DB
from core import welcome as wel

# initialisation des variables.
DEFAUT_PREFIX = "*"


VERSION = open("core/version.txt").read().replace("\n","")
TOKEN = open("token/token_getgems.txt", "r").read().replace("\n","")
client = commands.Bot(command_prefix = "{0}".format(DEFAUT_PREFIX))
NONE = open("help/cogs.txt","w")
NONE = open("help/help.txt","w")

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
	wel.memberremove(member)


####################### Commande help.py #######################

client.load_extension('help.help')

################### Core ############################

client.load_extension('core.utils')

####################### Commande gems.py #######################

client.load_extension('gems.gemsBase')

client.load_extension('gems.gemsPlay')

####################### Lancemement du bot ######################


client.run(TOKEN)
