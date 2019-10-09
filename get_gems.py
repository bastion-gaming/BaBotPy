import discord
from discord.ext import commands, tasks
from discord.ext.commands import Bot
from discord.utils import get

from DB import DB
import gems
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
	gems.loadItem()


@client.event
async def on_member_remove(member):
	wel.memberremove(member)


async def looped_task():
	counter = 0
	while not client.is_closed():
		if counter % 2 == 0 :
			activity = discord.Activity(type=discord.ActivityType.playing, name="▶ bastion-gaming.fr ◀")
			await client.change_presence(status=discord.Status.online, activity=activity)
		else:
			activity = discord.Activity(type=discord.ActivityType.playing, name="{}help".format(DEFAUT_PREFIX))
			await client.change_presence(status=discord.Status.online, activity=activity)
		GF.incrementebourse()
		counter += 1
		await asyncio.sleep(30)

####################### Commande help.py #######################

client.load_extension('help.help')

################### Core ############################

client.load_extension('core.utils')

####################### Commande gems.py #######################

client.load_extension('gems.gemsBase')

client.load_extension('gems.gemsPlay')

####################### Lancemement du bot ######################

client.loop.create_task(looped_task())
client.run(TOKEN)
