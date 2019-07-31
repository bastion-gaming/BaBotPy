import discord
import sqlite3
import welcome as wel
import datetime as t
import DB

# initialisation des variables.
DEFAUT_PREFIX = "!"

VERSION = open("version.txt").read().replace("\n","")
TOKEN = open("token", "r").read().replace("\n","")

client = discord.Client()
PREFIX = open("prefix.txt","r").read().replace('\n','')
bot = commands.Bot(command_prefix = "{0}".format(PREFIX))

# Au démarrage du bot.
@client.event
async def on_ready():
    print('Connecté avec le nom : {0.user}'.format(client))
    print('PREFIX = '+str(PREFIX))
    print('BastionBot '+VERSION+' | Core Module | >> Connecté !')
    await wel.on_ready()
    await gems.on_ready()
    DB.dbExist()

@client.event
async def on_member_join(member):
    await wel.autorole(member)
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
    DB.newPlayer(message.author.id)
client.run(TOKEN)
