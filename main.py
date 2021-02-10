import discord
from discord.ext import commands
from discord.ext.commands import Bot
import datetime as dt
from datetime import datetime
from DB import SQLite as sql
from core import stats as stat, level as lvl, welcome as wel, gestion as ge, roles
# from multimedia import notification_loop as notifL
import time

# initialisation des variables.
DEFAUT_PREFIX = "!"

VERSION = open("core/version.txt").read().replace("\n", "")
TOKEN = open("token/token.txt", "r").read().replace("\n", "")
PREFIX = open("core/prefix.txt", "r").read().replace("\n", "")

intents = discord.Intents(
    messages=True,
    guilds=True,
    members=True,
    emojis=True,
    voice_states=True,
    presences=True,
    guild_messages=True,
    dm_messages=True,
    reactions=True,
    guild_reactions=True,
    dm_reactions=True
)
client = commands.Bot(command_prefix = "{0}".format(PREFIX), intents=intents)
NONE = open("help/cogs.txt", "w")
NONE = open("help/help.txt", "w")

on_vocal = {}
on_vocal_cam = {}
on_vocal_stream = {}
jour = dt.date.today()

#####################################################

client.remove_command("help")


# Au démarrage du Bot.
@client.event
async def on_ready():
    print('Connecté avec le nom : {0.user}'.format(client))
    print('PREFIX = '+str(PREFIX))
    print('\nBastionBot '+VERSION)
    activity = discord.Activity(type=discord.ActivityType.playing, name="{0}help ◀ bastion-gaming.fr ▶".format(PREFIX))
    await client.change_presence(status=discord.Status.online, activity=activity)
    print(sql.init())
    flag = sql.checkField()
    if flag == 0:
        print("SQL >> Aucun champ n'a été ajouté, supprimé ou modifié.")
    elif "add" in flag:
        print("SQL >> Un ou plusieurs champs ont été ajoutés à la DB.")
    elif "sup" in flag:
        print("SQL >> Un ou plusieurs champs ont été supprimés de la DB.")
    elif "type" in flag:
        print("SQL >> Un ou plusieurs type ont été modifié sur la DB.")
    print('------\n')


####################### Commande help.py #######################

client.load_extension('help.help')

################### Core ############################

client.load_extension('core.utils')

################### Welcome #################################


@client.event
async def on_member_join(member):
    guild = client.get_guild(member.guild.id)
    if guild.system_channel != None:
        systemchannel = guild.system_channel
    else:
        systemchannel = 0
    await wel.memberjoin(member, systemchannel)


@client.event
async def on_member_remove(member):
    guild = client.get_guild(member.guild.id)
    if guild.system_channel != None:
        systemchannel = guild.system_channel
    else:
        systemchannel = 0
    await systemchannel.send(wel.memberremove(member))


####################### Stat ####################################


@client.event
async def on_voice_state_update(member, before, after):
    ID = member.id
    guild = client.get_guild(member.guild.id)
    if guild.id == wel.idBASTION:
        if guild.afk_channel != None:
            afkchannel = guild.afk_channel.id
        else:
            afkchannel = 0

        # Voice XP
        if after.channel != None and not (member.name in on_vocal) and after.channel.id != afkchannel:
            on_vocal[member.name] = time.time()
        elif (after.channel == None or after.channel.id == afkchannel) and member.name in on_vocal :
            time_on_vocal = round((time.time() - on_vocal[member.name])/60)
            print('{} as passé {} minutes en vocal !'.format(member.name, time_on_vocal))
            balXP = sql.valueAt(ID, "xp", "bastion")
            if balXP != 0:
                balXP = int(balXP[0])
            XP = balXP + int(time_on_vocal)
            sql.updateField(ID, "xp", XP, "bastion")
            await lvl.checklevelvocal(member)
            del on_vocal[member.name]

        # Cam XP
        if after.self_video and not (member.name in on_vocal_cam) and after.channel.id != afkchannel:
            on_vocal_cam[member.name] = time.time()
        elif ((not after.self_video) or after.channel.id == afkchannel) and member.name in on_vocal_cam :
            time_on_vocal_cam = round((time.time() - on_vocal_cam[member.name])/60)
            print('{} as passé {} minutes avec la caméra allumée !'.format(member.name, time_on_vocal_cam))
            balXP = sql.valueAt(ID, "xp", "bastion")
            if balXP != 0:
                balXP = int(balXP[0])
            XP = balXP + int(time_on_vocal_cam)
            sql.updateField(ID, "xp", XP, "bastion")
            await lvl.checklevelvocal(member)
            del on_vocal_cam[member.name]

        # Stream XP
        if after.self_stream and not (member.name in on_vocal_stream) and after.channel.id != afkchannel:
            on_vocal_stream[member.name] = time.time()
        elif ((not after.self_stream) or after.channel.id == afkchannel) and member.name in on_vocal_stream :
            time_on_vocal_stream = round((time.time() - on_vocal_stream[member.name])/60)
            print('{} as passé {} minutes en stream !'.format(member.name, time_on_vocal_stream))
            balXP = sql.valueAt(ID, "xp", "bastion")
            if balXP != 0:
                balXP = int(balXP[0])
            XP = balXP + int(time_on_vocal_stream)
            sql.updateField(ID, "xp", XP, "bastion")
            await lvl.checklevelvocal(member)
            del on_vocal_stream[member.name]


@client.event
async def on_message(message):
    if not (message.author.bot or message.content.startswith(PREFIX)) :
        if message.guild.id == wel.idBASTION:
            if not ge.checkInfo(message.author.id):
                member = message.guild.get_member(message.author.id)
                await roles.addrole(member, "Nouveau")
            await stat.countMsg(message)
            await lvl.checklevel(message)
            await client.process_commands(message)
        else:
            await client.process_commands(message)
    else:
        await client.process_commands(message)


# @client.event
# async def on_reaction_add(message, user):
#     if not (message.author.bot or message.content.startswith(PREFIX)) :
#         if message.guild.id == wel.idBASTION:
#             await client.process_commands(message)
#         else:
#             await client.process_commands(message)
#     else:
#         await client.process_commands(message)
#
#
# @client.event
# async def on_reaction_remove(message, user):
#     if not (message.author.bot or message.content.startswith(PREFIX)) :
#         if message.guild.id == wel.idBASTION:
#             await client.process_commands(message)
#         else:
#             await client.process_commands(message)
#     else:
#         await client.process_commands(message)

####################### Commande stats.py #######################

client.load_extension('core.stats')

####################### Commande roles.py #######################

client.load_extension('core.roles')

####################### Commande level.py #######################

client.load_extension('core.level')

###################### Commande gestion.py #####################

client.load_extension('core.gestion')

###################### Commande notification.py ################

# client.load_extension('multimedia.notification')

###################### Commande vocal.py ########################

# client.load_extension('multimedia.vocal')

##################### Commande images.py #####################

# client.load_extension('multimedia.images')

###################### Commande parrain.py ########################

client.load_extension('core.parrain')

##################### Commande kaamelott.py #####################

client.load_extension('kaamelott.kaamelott')

####################### Lancemement du bot ######################


try:
    client.run(TOKEN)
except (KeyboardInterrupt, SystemExit):
    pass
