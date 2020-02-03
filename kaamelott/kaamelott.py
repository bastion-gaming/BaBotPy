import discord
import random as r
from discord.ext import commands


class Kaamelott(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.autheur = {"ANGARADE": (0, 1), "ANNA": (2, 4), "ATILA": (5, 7), "CALOGRENANT": (8, 9),
        "CRYDA DE TINTAGEL": (10, 10), "DAGONET": (11, 11), "LA DAME DU LAC": (12, 13),
        "LE PÈRE BLAISE": (14, 18), "BOHORT": (19, 27), "LE ROI DE BURGONDE": (28, 33),
        "DEMETRA": (34, 35), "GAUVAIN": (36, 39), "GUENIÈVRE": (40, 45), "KADOC": (46, 53),
        "LANCELOT": (54, 59), "LE MAITRE D'ARME": (60, 67), "LE TAVERNIER": (68, 72),
        "VENEC": (73, 80), "YVAIN": (81, 88), "KARADOC": (89, 95), "PERCEVAL": (96, 116),
        "GUETHENOC": (117, 119), "LÉODAGAN": (120, 124), "LOTH": (125, 132), "ARTHUR": (133, 138),
        "ROPARZH": (139, 141), "MERLIN": (142, 149)}
        return

    @commands.command(pass_context=True)
    async def personnage(self, ctx):
        """Liste des personnages de Kaamelott ayant une citation"""
        msg = "**Voici la liste des personnages de Kaamelott ayant une citation :**\n"
        for c in self.autheur :
            msg += c + " avec " + str(- self.autheur[c][0] + self.autheur[c][1] + 1) + " citation.s\n"
        await ctx.send(msg)

    @commands.command(pass_context=True)
    async def citation(self, ctx, *, personnage = None):
        """**[personnage]** | Donne une citation random ou d'un personnage en particulier"""
        f = open("kaamelott/citation.txt", "r").read().split('\n')
        if personnage == None :
            quote = f[r.randint(0, len(f)-2)].split('//')
            await ctx.send(quote[0]+"\n\n*"+quote[1]+"*")
        else :
            perso = personnage.upper()
            try :
                quote = f[r.randint(self.autheur[perso][0], self.autheur[perso][1])].split('//')
                await ctx.send(quote[0]+"\n\n*"+quote[1]+"*")
            except ValueError:
                await ctx.send("Le nom du personnage est inconnue")
                pass


def setup(bot):
    bot.add_cog(Kaamelott(bot))
    open("help/cogs.txt", "a").write("Kaamelott\n")
