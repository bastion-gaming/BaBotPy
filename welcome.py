# Utilisation de Pytho 3.6
import discord
import time as t
from discord.ext import commands
import sqlite3

client = discord.Client()

@client.event  # event decorator/wrapper. More on decorators here: https://pythonprogramming.net/decorators-intermediate-python-tutorial/
async def on_ready():  # method expected by client. This runs once when connected
    print(f'BastionBot | Welcome Module | Python version | >> Connecté !')  # notification of login.
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
async def on_member_join(member):
    role = discord.utils.get(member.guild.roles, name="Joueurs")
    await member.add_roles(role)
    time = t.time()
    data = sqlite3.connect('connect.db')
    c = data.cursor()
    c.execute("""SELECT name FROM users WHERE id = member.id""")
    if c.fetchone() == None:
        # si le l'id est inconnue c'est une nouvelle personne qui se connecte !
        c.execute(""" INSERT INTO users VALUES(?,?,?) """, (member.id,{member.mention}, time))
        c.execute("""UPDATE compte SET nombre = nombre +1 WHERE ID = total""") #incrémente de 1 à chaque nouvelle personne
        c.commit()
        data.close()
        msg = f""":black_small_square:Bienvenue {member.mention} sur Bastion!:black_small_square: \n\n\nNous sommes ravis que tu aies rejoint notre communauté !\nTu es attendu :\n\n:arrow_right: Sur #⌈:closed_book:⌋•règles\n:arrow_right: Sur #⌈:ledger:⌋•liste-salons\n\n====================="""
    else :
        # si le nom est déjà dans la BDD on ne le recompte pas une deuxième fois
        msg = f"""Ravis de te revoir parmis nous {member.mention} !!"""
    channel = client.get_channel(478003352551030798)
    await channel.send(msg)

@client.event
async def on_member_remove(member):
    channel = client.get_channel(417445503110742048)
    await channel.send(f"""{member.mention} nous a quitté, pourtant si jeune...""")
