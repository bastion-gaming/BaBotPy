import discord
from discord.ext import commands, tasks
from discord.ext.commands import Bot
from discord.utils import get
import datetime as t
from datetime import datetime

from DB import DB
from gems import gemsFonctions as GF
from core import welcome as wel

import asyncio
import aiohttp
import json
import re
import time

# initialisation des variables.
DEFAUT_PREFIX = "*"


VERSION = open("core/version.txt").read().replace("\n","")
TOKEN = open("token/token_getgems.txt", "r").read().replace("\n","")
client = commands.Bot(command_prefix = "{0}".format(DEFAUT_PREFIX))
NONE = open("help/cogs.txt","w")
NONE = open("help/help.txt","w")

jour = t.date.today()

client.remove_command("help")

# Au démarrage du Bot.
@client.event
async def on_ready():
	print('Connecté avec le nom : {0.user}'.format(client))
	print('PREFIX = '+str(DEFAUT_PREFIX))
	GF.setglobalguild(client.get_guild(wel.idServBot))
	print('\nBastionBot '+VERSION)
	print('------\n')
	GF.checkDB_Gems()
	# GF.checkDB_Session()
	GF.loadItem(True)


@client.event
async def on_member_remove(member):
	wel.memberremove(member)


####################### Commande help.py #######################

client.load_extension('help.help')

################### Core ############################

client.load_extension('core.utils')

####################### Commande gems.py #######################

client.load_extension('gems.gemsFonctions')

client.load_extension('gems.gemsBase')

client.load_extension('gems.gemsPlay')

# client.load_extension('gems.gemsFight')

if (jour.month == 10 and jour.day >= 23) or (jour.month == 11 and jour.day <= 10):
	client.load_extension('gems.gemsEvent')

#---------------------------------------------------------------
#---------------------------------------------------------------
async def looped_task():
	await client.wait_until_ready()
	counter = 0
	while not client.is_closed():
		if counter % 2 == 0 :
			activity = discord.Activity(type=discord.ActivityType.playing, name="▶ bastion-gaming.fr ◀")
			await client.change_presence(status=discord.Status.online, activity=activity)
		else:
			activity = discord.Activity(type=discord.ActivityType.playing, name="{}help".format(DEFAUT_PREFIX))
			await client.change_presence(status=discord.Status.online, activity=activity)
		# GF.incrementebourse()
		if counter == 0:
			GF.setglobalguild(client.get_guild(wel.idServBot))
			GF.loadItem(True)
		else:
			if DB.spam(wel.idGetGems,GF.couldown_12h, "bourse", "DB/bastionDB"):
				GF.loadItem()
		print(counter)
		counter += 1
		await asyncio.sleep(30)
#---------------------------------------------------------------
#---------------------------------------------------------------

####################### Lancemement du bot ######################

client.loop.create_task(looped_task())
client.run(TOKEN)
