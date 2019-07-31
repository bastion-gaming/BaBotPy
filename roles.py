# Utilisation de Pytho 3.6
import discord
import time as t
from discord.ext import commands
import sqlite3

client = discord.Client()

@client.event  # event decorator/wrapper. More on decorators here: https://pythonprogramming.net/decorators-intermediate-python-tutorial/
async def on_ready():  # method expected by client. This runs once when connected
    print(f'| Roles Module | >> Connecté !')  # notification of login.

async def autorole(member):
    role = discord.utils.get(member.guild.roles, name="Joueurs")
    await member.add_roles(role)


async def create(message, meco):
#    """Commande !create game <nom du jeu>, <Categorie du jeu: combat/societe/tirs/voiture/rpg/sandbox/strategie/divers>"""
    mecoS = meco.split(',')
    guild = message.guild
    member = message.author
    rolesearch = discord.utils.get(member.guild.roles, name=mecoS[0])
    if rolesearch == None:
        await guild.create_role(name=mecoS[0])
        await message.channel.send("Le jeu '"+mecoS[0]+"' a été créé")

        if mecoS[1] != None:
            rolesearch = discord.utils.get(member.guild.roles, name=mecoS[0])
            mecoS[1] = mecoS[1].replace(" ", "")
            mecoS[1] = mecoS[1].lower()

            if mecoS[1] == "combat":
                channel = guild.get_channel(589944955800256515)
            elif mecoS[1] == "societe":
                channel = guild.get_channel(589945591203889152)
            elif mecoS[1] == "tirs":
                channel = guild.get_channel(589946246437797888)
            elif mecoS[1] == "voiture":
                channel = guild.get_channel(589946276540448821)
            elif mecoS[1] == "rpg":
                channel = guild.get_channel(589946305917222916)
            elif mecoS[1] == "sandbox":
                channel = guild.get_channel(589946380416581632)
            elif mecoS[1] == "strategie":
                channel = guild.get_channel(589953946639007764)
            else:
                channel = guild.get_channel(590664052318142474)
            await channel.set_permissions(rolesearch, overwrite=discord.PermissionOverwrite(read_messages=True))
            await channel.send(f"Ajout d'un nouveau jeu dans la catégorie {channel.mention}: {rolesearch.mention}")
    else:
        await message.channel.send("Le jeu '"+mecoS[0]+"' existe déjà")
