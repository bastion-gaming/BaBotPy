import json
import os
from typing import Callable, TypeVar

from discord.ext import commands
from core.exceptions import *

from core import file

T = TypeVar("T")


def is_owner() -> Callable[[T], T]:
    """
    Il s'agit d'une vérification personnalisée pour voir si l'utilisateur exécutant la commande est un propriétaire du bot.
    """

    async def predicate(context: commands.Context) -> bool:
        data = file.json_read(f"{os.path.realpath(os.path.dirname(__file__))}/../config.json")
        if context.author.id not in data["owners"]:
            raise UserNotOwner
        return True

    return commands.check(predicate)