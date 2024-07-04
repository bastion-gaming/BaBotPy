import os, sys, platform
import asyncio
import logging
import random
import time, datetime

import discord
from discord.ext import commands, tasks
from discord.ext.commands import Bot, Context

from core import file, exceptions, welcome as wel
from core import gestion as ge, level as lvl

################################################
# Définition des variables
# ========================
on_vocal = {}
on_vocal_cam = {}
on_vocal_stream = {}

intents = discord.Intents.all()
# intents = discord.Intents.default()
# intents.members = True
# intents.messages = True
# intents.message_content = True
# intents.reactions = True
# intents.presences = True

bot = Bot(
    command_prefix=commands.when_mentioned_or(ge.PREFIX),
    intents=intents,
    help_command=None,
)

################################################
# Journalisation
# ==============
class LoggingFormatter(logging.Formatter):
    # Colors
    black = "\x1b[30m"
    red = "\x1b[31m"
    green = "\x1b[32m"
    yellow = "\x1b[33m"
    blue = "\x1b[34m"
    gray = "\x1b[38m"
    # Styles
    reset = "\x1b[0m"
    bold = "\x1b[1m"

    COLORS = {
        logging.DEBUG: gray + bold,
        logging.INFO: blue + bold,
        logging.WARNING: yellow + bold,
        logging.ERROR: red,
        logging.CRITICAL: red + bold,
    }

    def format(self, record):
        log_color = self.COLORS[record.levelno]
        format = "(black){asctime}(reset) (levelcolor){levelname:<8}(reset) (green){name}(reset) {message}"
        format = format.replace("(black)", self.black + self.bold)
        format = format.replace("(reset)", self.reset)
        format = format.replace("(levelcolor)", log_color)
        format = format.replace("(green)", self.green + self.bold)
        formatter = logging.Formatter(format, "%Y-%m-%d %H:%M:%S", style="{")
        return formatter.format(record)


logger = logging.getLogger("discord_bot")
logger.setLevel(logging.INFO)
handler_formatter = logging.Formatter(
    "[{asctime}] {levelname:<8} {message}", "%Y-%m-%d %H:%M:%S", style="{"
)

# Console handler
console_handler = logging.StreamHandler()
console_handler.setFormatter(LoggingFormatter())
# File handler
LOG_PATH = "logs/"
LOG_FILE = "discord.log"
if file.exist(f"{LOG_PATH}{LOG_FILE}"):
    data = file.read(f"{LOG_PATH}{LOG_FILE}")
    now = datetime.date.today()
    nowtime = datetime.datetime.now().strftime("%H-%M-%S")
    LOG_NEW = f"{LOG_PATH}discord-{now}_{nowtime}.log"
    file.create(LOG_NEW)
    file.write(LOG_NEW, data)

file_handler = logging.FileHandler(filename=f"{LOG_PATH}{LOG_FILE}", encoding="utf-8", mode="w")
file_handler.setFormatter(handler_formatter)

# Add the handlers
logger.addHandler(console_handler)
logger.addHandler(file_handler)
bot.logger = logger


################################################
# Bot
# ===================
bot.config = ge.CONFIG

@bot.event
async def on_ready() -> None:
    """
    Le code de cet événement est exécuté lorsque le bot est prêt.
    """
    bot.logger.info(f"Connecté avec le nom {bot.user.name}")
    bot.logger.info(f"Bot version: {ge.VERSION}")
    bot.logger.info(f"{ge.CONFIG['api']['name']} version: {ge.CONFIG['api']['version']}")
    bot.logger.info("-------------------")
    bot.logger.info(f"discord.py version: {discord.__version__}")
    bot.logger.info(f"Python version: {platform.python_version()}")
    bot.logger.info(f"Running on: {platform.system()} {platform.release()} ({os.name})")
    bot.logger.info("-------------------")
    status_task.start()
    if ge.CONFIG["sync_commands_globally"]:
        bot.logger.info("Synchroniser les commandes globalement...")
        await bot.tree.sync()

################################################
@tasks.loop(minutes=1.0)
async def status_task() -> None:
    """
    Configurez la tâche d'état du bot.
    """
    statuses = ["spinelle.eu", "", ""]
    # await bot.change_presence(activity=discord.watching(random.choice(statuses)))
    activity = discord.Activity(type=discord.ActivityType.watching, name="spinelle.eu")
    await bot.change_presence(status=discord.Status.online, activity=activity)

################################################
# Welcome
@bot.event
async def on_member_join(member) -> None:
    guild = bot.get_guild(member.guild.id)
    if guild.system_channel != None:
        systemchannel = guild.system_channel
    else:
        systemchannel = 0
    await wel.memberjoin(member, systemchannel)


@bot.event
async def on_member_remove(member) -> None:
    guild = bot.get_guild(member.guild.id)
    if guild.system_channel != None:
        systemchannel = guild.system_channel
    else:
        systemchannel = 0
    await wel.memberremove(member, systemchannel)


################################################
# Message et XP
@bot.event
async def on_message(message: discord.Message) -> None:
    if message.author == bot.user or message.author.bot:
        return
    PREFIX_CHECK = False
    for prefixstart in ge.PREFIX_LIST:
        if message.content.startswith(prefixstart):
            PREFIX_CHECK = True
    if not PREFIX_CHECK:
        try:
            if message.guild.id in ge.guildID:
                lvl.xpmsg(message)
                await lvl.checklevel(message)
        except:
            pass
    await bot.process_commands(message)


@bot.event
async def on_voice_state_update(member, before, after) -> None:
    ID = member.id
    guild = bot.get_guild(member.guild.id)
    if guild.id in ge.guildID:
        if guild.afk_channel != None:
            afkchannel = guild.afk_channel.id
        else:
            afkchannel = 0

        # Voice XP
        if after.channel != None and not (member.name in on_vocal) and after.channel.id != afkchannel:
            on_vocal[member.name] = time.time()
        elif (after.channel == None or after.channel.id == afkchannel) and member.name in on_vocal :
            time_on_vocal = round((time.time() - on_vocal[member.name])/60)
            bot.logger.info('{} as passé {} minutes en vocal !'.format(member.name, time_on_vocal))
            lvl.addxp_voc(ID, time_on_vocal)
            await lvl.checklevelvocal(member)
            del on_vocal[member.name]

        # Cam XP
        if after.self_video and not (member.name in on_vocal_cam):
            on_vocal_cam[member.name] = time.time()
        elif (after.channel == None or not after.self_video) and member.name in on_vocal_cam :
            time_on_vocal_cam = round((time.time() - on_vocal_cam[member.name])/60)
            bot.logger.info('{} as passé {} minutes avec la caméra allumée !'.format(member.name, time_on_vocal_cam))
            lvl.addxp_voc(ID, time_on_vocal_cam)
            await lvl.checklevelvocal(member)
            del on_vocal_cam[member.name]

        # Stream XP
        if after.self_stream and not (member.name in on_vocal_stream):
            on_vocal_stream[member.name] = time.time()
        elif (after.channel == None or not after.self_stream) and member.name in on_vocal_stream :
            time_on_vocal_stream = round((time.time() - on_vocal_stream[member.name])/60)
            bot.logger.info('{} as passé {} minutes en stream !'.format(member.name, time_on_vocal_stream))
            lvl.addxp_voc(ID, time_on_vocal_stream)
            await lvl.checklevelvocal(member)
            del on_vocal_stream[member.name]


@bot.event
async def on_raw_reaction_add(payload) -> None:
    if payload.guild_id in ge.guildID:
        ID = payload.user_id
        lvl.addxp(ID, 1)
        lvl.addreaction(ID, 1)
        bot.logger.info("Ajout d'une réaction")


@bot.event
async def on_raw_reaction_remove(payload) -> None:
    if payload.guild_id in ge.guildID:
        ID = payload.user_id
        lvl.addxp(ID, -1)
        lvl.addreaction(ID, -1)
        bot.logger.info("Retrait d'une réaction")


################################################
@bot.event
async def on_command_completion(context: Context) -> None:
    full_command_name = context.command.qualified_name
    split = full_command_name.split(" ")
    executed_command = str(split[0])
    if context.guild is not None:
        bot.logger.info(
            f"Commande {executed_command} exécutée dans {context.guild.name} (ID: {context.guild.id}) par {context.author} (ID: {context.author.id})"
        )
    else:
        bot.logger.info(
            f"Commande {executed_command} exécutée par {context.author} (ID: {context.author.id}) dans les DMs"
        )


################################################
# Exceptions et Erreurs
@bot.event
async def on_command_error(context: Context, error) -> None:
    if isinstance(error, commands.CommandOnCooldown):
        minutes, seconds = divmod(error.retry_after, 60)
        hours, minutes = divmod(minutes, 60)
        hours = hours % 24
        embed = discord.Embed(
            description=f"**Veuillez ralentir** - Vous pouvez réutiliser cette commande dans {f'{round(hours)} hours' if round(hours) > 0 else ''} {f'{round(minutes)} minutes' if round(minutes) > 0 else ''} {f'{round(seconds)} seconds' if round(seconds) > 0 else ''}.",
            color=0xE02B2B,
        )
        await context.send(embed=embed)
    elif isinstance(error, exceptions.UserNotOwner):
        """
        Comme ci-dessus, juste pour la vérification @checks.is_owner().
        """
        embed = discord.Embed(
            description="Vous n'êtes pas le propriétaire du bot!", color=0xE02B2B
        )
        await context.send(embed=embed)
        if context.guild:
            bot.logger.warning(
                f"{context.author} (ID: {context.author.id}) a essayé d'exécuter une commande propriétaire uniquement dans la guilde {context.guild.name} (ID: {context.guild.id}), mais l'utilisateur n'est pas propriétaire du bot."
            )
        else:
            bot.logger.warning(
                f"{context.author} (ID: {context.author.id}) a essayé d'exécuter une commande propriétaire uniquement dans les DM du bot, mais l'utilisateur n'est pas propriétaire du bot."
            )
    elif isinstance(error, commands.MissingPermissions):
        embed = discord.Embed(
            description="Il vous manque les autorisations `"
            + ", ".join(error.missing_permissions)
            + "` pour exécuter cette commande!",
            color=0xE02B2B,
        )
        await context.send(embed=embed)
    elif isinstance(error, commands.BotMissingPermissions):
        embed = discord.Embed(
            description="Il vous manque les autorisations `"
            + ", ".join(error.missing_permissions)
            + "` pour exécuter pleinement cette commande!",
            color=0xE02B2B,
        )
        await context.send(embed=embed)
    elif isinstance(error, commands.MissingRequiredArgument):
        embed = discord.Embed(
            title="Erreur!",
            description=str(error).capitalize(),
            color=0xE02B2B,
        )
        await context.send(embed=embed)
    else:
        raise error


################################################
# Extensions
async def load_extensions() -> None:
    """
    Le code de cette fonction est exécuté chaque fois que le bot démarre.
    """
    for file in os.listdir(f"{os.path.realpath(os.path.dirname(__file__))}/extensions"):
        if file.endswith(".py"):
            extension = file[:-3]
            try:
                await bot.load_extension(f"extensions.{extension}")
                bot.logger.info(f"Extension '{extension}' chargée")
            except Exception as e:
                exception = f"{type(e).__name__}: {e}"
                bot.logger.error(f"Échec du chargement de l'extension {extension}\n{exception}")

################################################
asyncio.run(load_extensions())
bot.run(ge.TOKEN)
