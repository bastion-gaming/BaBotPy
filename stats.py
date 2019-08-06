import random as r
import datetime as dt
import DB
from discord.ext import commands
from discord.ext.commands import bot
from discord.utils import get
import discord

async def countMsg(message):
	id = message.author.id
	DB.updateField(id, "nbMsg", int(DB.valueAt(id, "nbMsg")+1))
	return(DB.valueAt(id, "nbMsg"))
