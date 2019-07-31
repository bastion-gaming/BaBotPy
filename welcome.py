# Utilisation de Pytho 3.6
import discord
import time as t
from discord.ext import commands
import sqlite3

client = discord.Client()

@client.event  # event decorator/wrapper. More on decorators here: https://pythonprogramming.net/decorators-intermediate-python-tutorial/
async def on_ready():  # method expected by client. This runs once when connected
    print(f'| Welcome Module | >> Connecté !')  # notification of login.
    #-------------
    #data = sqlite3.connect('connect.db')
    #c = data.cursor()
    #c.execute(""" CREATE TABLE users(id INTEGER PRIMARY KEY, name TEXT, time DATE) """)
    #c.commit()
    #data.close()
    #---------------
    # Le code ici est une mauvaise idée car il crée une nouvelle table à chaque connexion. mieux vaut créé sa propre table
    # de son coté et uniquement l'update apres.

@client.event
async def on_member_remove(member):
    channel = client.get_channel(417445503110742048)
    await channel.send(f"""{member.mention} nous a quitté, pourtant si jeune...""")
#=======
    await message.channel.send(f'{number[0]} utilisateurs inscrit')
#>>>>>>> 7b6ad3b766efcde72db729b9d00f4f9290970995
