# Utilisation de Pytho 3.6
import discord
import time as t
from discord.ext import commands
import sqlite3

client = discord.Client()

@client.event  # event decorator/wrapper. More on decorators here: https://pythonprogramming.net/decorators-intermediate-python-tutorial/
async def on_ready():  # method expected by client. This runs once when connected
    print(f'BastionBot | Welcome Module | >> Connecté !')  # notification of login.
    #-------------
    #data = sqlite3.connect('connect.db')
    #c = data.cursor()
    #c.execute(""" CREATE TABLE users(id INTEGER PRIMARY KEY, name TEXT, time DATE) """)
    #c.commit()
    #data.close()
    #---------------
    # Le code ici est une mauvaise idée car il crée une nouvelle table à chaque connexion. mieux vaut créé sa propre table
    # de son coté et uniquement l'update apres.

async def autorole(member):
    role = discord.utils.get(member.guild.roles, name="Joueurs")
    await member.add_roles(role)


async def count(message):
    data = sqlite3.connect('connect.db')
    c = data.cursor()
    c.execute("""SELECT COUNT(id) FROM users""")
    number = c.fetchone()
    data.close()
    if number[0] == 0:
        await message.channel.send('Aucun utilisaeur enregistrer dans la BDD')
    if number[0] == 1:
        await message.channel.send(f'{number[0]} utilisateur inscrit')
    else :
<<<<<<< HEAD
        # si le nom est déjà dans la BDD on ne le recompte pas une deuxième fois
        msg = f"""Ravis de te revoir parmis nous {member.mention} !!"""
    channel = client.get_channel(478003352551030798)
    await channel.send(msg)

@client.event
async def on_member_remove(member):
    channel = client.get_channel(417445503110742048)
    await channel.send(f"""{member.mention} nous a quitté, pourtant si jeune...""")
=======
        await message.channel.send(f'{number[0]} utilisateurs inscrit')
>>>>>>> 7b6ad3b766efcde72db729b9d00f4f9290970995
