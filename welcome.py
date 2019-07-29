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
        await message.channel.send(f'{number[0]} utilisateurs inscrit')
