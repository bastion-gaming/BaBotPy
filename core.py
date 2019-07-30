import discord
import welcome as wel
import gems
import DB

# initialisation des variables.
DEFAUT_PREFIX = "!"

VERSION = open("version.txt").read().replace("\n","")
TOKEN = open("token", "r").read().replace("\n","")

client = discord.Client()
PREFIX = DEFAUT_PREFIX
# Au démarrage du bot.
@client.event
async def on_ready():
    print('Connecté avec le nom : {0.user}'.format(client))
    print('BastionBot | Core Module | Python version | >> Connecté !')
    await gems.on_ready()
    DB.dbExist()


#Quand il y'a un message
@client.event
async def on_message(message):




client.run(TOKEN)
