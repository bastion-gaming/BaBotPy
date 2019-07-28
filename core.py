import discord
import welcome as wel
import gems

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
    await wel.on_ready()
    await gems.on_ready()

#Quand il y'a un message
@client.event
async def on_message(message):
    meco = message.content
    if message.author == client.user:
        return

    if meco.startswith(PREFIX+"coreInfo"):
        await message.channel.send('Actuellement version **'+VERSION+'**')

    elif meco.startswith(PREFIX+"begin"):
        await gems.begin(message)

    elif meco.startswith(PREFIX+"bal"):
        await gems.bal(message)



client.run(TOKEN)
