import discord
from discord.ext import commands
from discord.ext.commands import bot
from operator import itemgetter
from core import gestion as ge
from gems import gemsFonctions as GF
from languages import lang as lang_P
import gg_lib as gg
import datetime as dt


class GemsSuccess(commands.Cog):

    def __init__(self, ctx):
        return(None)

    @commands.command(pass_context=True)
    async def stats(self, ctx, Nom = None):
        """
        Affichage des statistiques du joueur.
        """
        ID = ctx.author.id
        param = dict()
        param["ID"] = ID
        if ge.permission(ctx, ge.Inquisiteur):
            param["nom"] = Nom
            if Nom == None:
                Nom = ctx.author.name
            else:
                Nom = ctx.guild.get_member(ge.nom_ID(Nom)).name
        else:
            param["nom"] = "None"
            Nom = ctx.author.name

        ge.socket.send_string(gg.std_send_command("stats", ID, ge.name_pl, param))
        tab = GF.msg_recv()
        lang = tab[1]
        if tab[0] == "NOK":
            await ctx.channel.send(lang_P.forge_msg(lang, "WarningMsg", None, False, 0))
            return False
        elif tab[0] == "WarningMsg":
            await ctx.channel.send(tab[1])
            return False
        ltab = len(tab)
        StatList = []
        for i in range(2, ltab):
            tab[i] = tab[i].replace("(", "")
            tab[i] = tab[i].replace(")", "")
            tab[i] = tab[i].replace("'", "")
            tab[i] = tab[i].split(", ")
            StatList.append((tab[i][0], tab[i][1], tab[i][2]))
        StatList = sorted(StatList, key=itemgetter(2))
        StatList = sorted(StatList, key=itemgetter(1))
        desc = ""           # Statistique non pris en charge
        descGeneral = ""     # bal, baltop, inv, market, divers
        descBuy = ""        # buy
        descSell = ""       # sell
        descDon = ""        # pay, give
        descForge = ""      # forge
        descBank = ""       # bank, stealing, crime, gamble
        descMine = ""       # mine
        descDig = ""        # dig
        descFish = ""       # fish
        descSlots = ""      # slots
        descBoxes = ""      # boxes
        descHothouse = ""   # hothouse
        descCooking = ""    # cooking
        descFerment = ""    # ferment
        for x in StatList:
            y = x[2].split(" | ")
            if x[1] == "bal" or x[1] == "inv" or x[1] == "market" or x[1] == "baltop":
                if x[2] == x[1]:
                    descGeneral += "{2} **{1}** `{0}`\n\n".format(x[0], x[2], lang_P.forge_msg(lang, "stats", None, False, 15))

            elif x[1] == "buy":
                if x[2] == x[1]:
                    descBuy += "{2} **{1}** `{0}`\n\n".format(x[0], x[2], lang_P.forge_msg(lang, "stats", None, False, 15))
                else:
                    for i in range(1, len(y)):
                        if y[i] == "item":
                            descBuy += "{0} ".format(lang_P.forge_msg(lang, "stats", None, False, 1))
                        elif y[i] == "dépense":
                            descBuy += "{0} ".format(lang_P.forge_msg(lang, "stats", None, False, 16))
                        else:
                            descBuy += y[i] + " "
                        if i == len(y)-1:
                            descBuy += ": `{0}`\n\n".format(x[0])

            elif x[1] == "sell":
                if x[2] == x[1]:
                    descSell += "{2} **{1}** `{0}`\n\n".format(x[0], x[2], lang_P.forge_msg(lang, "stats", None, False, 15))
                else:
                    for i in range(1, len(y)):
                        if y[i] == "item":
                            descSell += "{0} ".format(lang_P.forge_msg(lang, "stats", None, False, 2))
                        elif y[i] == "gain":
                            descSell += "{0} ".format(lang_P.forge_msg(lang, "stats", None, False, 17))
                        else:
                            descSell += y[i] + " "
                        if i == len(y)-1:
                            descSell += ": `{0}`\n\n".format(x[0])

            elif x[1] == "pay" or x[1] == "give":
                if x[2] == x[1]:
                    descDon += "{2} **{1}** `{0}`\n\n".format(x[0], x[2], lang_P.forge_msg(lang, "stats", None, False, 15))
                else:
                    for i in range(0, len(y)):
                        if x[1] == "give" and y[i] == "item":
                            descDon += "{0} {1} ".format(lang_P.forge_msg(lang, "stats", None, False, 3), y[i+1])
                        elif y[i] == "nb items" or y[i] == "nb gems":
                            descDon += "{0} {1} ".format(lang_P.forge_msg(lang, "stats", None, False, 3), lang_P.forge_msg(lang, "stats", None, False, 21))
                            if y[i] == "nb items":
                                descDon += "items "
                            else:
                                descDon += "gems "
                        elif y[i] != "pay" and y[i] != "give":
                            descDon += y[i] + " "
                        if i == len(y)-1:
                            descDon += ": `{0}`\n\n".format(x[0])

            elif x[1] == "forge":
                if x[2] == x[1]:
                    descForge += "{2} **{1}** `{0}`\n\n".format(x[0], x[2], lang_P.forge_msg(lang, "stats", None, False, 15))
                else:
                    for i in range(1, len(y)):
                        if y[i] == "item":
                            descForge += "{0} ".format(lang_P.forge_msg(lang, "stats", None, False, 4))
                        elif y[i] == "nb items":
                            descForge += "{0} {1} items ".format(lang_P.forge_msg(lang, "stats", None, False, 4), lang_P.forge_msg(lang, "stats", None, False, 21))
                        else:
                            descForge += y[i] + " "
                        if i == len(y)-1:
                            descForge += ": `{0}`\n\n".format(x[0])

            elif x[1] == "bank" or x[1] == "stealing" or x[1] == "crime" or x[1] == "gamble":
                if x[2] == x[1] or x[2] == "bank saving":
                    descBank += "{2} **{1}** `{0}`\n\n".format(x[0], x[2], lang_P.forge_msg(lang, "stats", None, False, 15))
                else:
                    for i in range(0, len(y)):
                        if x[1] == "bank" and y[i] == "gain":
                            descBank += "{0} {1} ".format(lang_P.forge_msg(lang, "stats", None, False, 17), lang_P.forge_msg(lang, "stats", None, False, 22))
                        elif x[1] == "stealing" and y[i] == "gain":
                            descBank += "{0} {1} ".format(lang_P.forge_msg(lang, "stats", None, False, 17), lang_P.forge_msg(lang, "stats", None, False, 24))
                        elif x[1] == "gamble":
                            if y[i] == "win":
                                descBank += "Gamble {0} ".format(lang_P.forge_msg(lang, "stats", None, False, 23))
                            elif y[i] == "max":
                                descBank += "{0} ".format(lang_P.forge_msg(lang, "stats", None, False, 29))
                            elif y[i] == "gain" or y[i] == "perte":
                                if y[i] == "gain":
                                    descBank += "{0} ".format(lang_P.forge_msg(lang, "stats", None, False, 17))
                                elif y[i] == "perte":
                                    descBank += "{0} ".format(lang_P.forge_msg(lang, "stats", None, False, 18))
                                descBank += "_gamble_ "
                        elif x[1] == "crime" and y[i] == "gain":
                            descBank += "{0} _crime_ ".format(lang_P.forge_msg(lang, "stats", None, False, 17))
                        elif x[1] != "bank" and x[1] != "crime" and x[1] != "stealing":
                            descBank += y[i] + " "
                        if i == len(y)-1:
                            descBank += ": `{0}`\n\n".format(x[0])

            elif x[1] == "mine":
                if x[2] == x[1]:
                    descMine += "{2} **{1}** `{0}`\n\n".format(x[0], x[2], lang_P.forge_msg(lang, "stats", None, False, 15))
                else:
                    for i in range(1, len(y)):
                        if y[i] == "item":
                            descMine += "{0} ".format(lang_P.forge_msg(lang, "stats", None, False, 6))
                        elif y[i] == "broken":
                            descMine += "{0} ".format(lang_P.forge_msg(lang, "stats", [y[i+1]], False, 19))
                        elif y[1] != "broken":
                            descMine += y[i] + " "
                        if i == len(y)-1:
                            descMine += ": `{0}`\n\n".format(x[0])

            elif x[1] == "fish":
                if x[2] == x[1]:
                    descFish += "{2} **{1}** `{0}`\n\n".format(x[0], x[2], lang_P.forge_msg(lang, "stats", None, False, 15))
                else:
                    for i in range(1, len(y)):
                        if y[i] == "item":
                            descFish += "{0} ".format(lang_P.forge_msg(lang, "stats", None, False, 7))
                        elif y[i] == "broken":
                            descFish += "{0} ".format(lang_P.forge_msg(lang, "stats", [y[i+1]], False, 19))
                        elif y[1] != "broken":
                            descFish += y[i] + " "
                        if i == len(y)-1:
                            descFish += ": `{0}`\n\n".format(x[0])

            elif x[1] == "dig":
                if x[2] == x[1]:
                    descDig += "{2} **{1}** `{0}`\n\n".format(x[0], x[2], lang_P.forge_msg(lang, "stats", None, False, 15))
                else:
                    for i in range(1, len(y)):
                        if y[i] == "item":
                            descDig += "{0} ".format(lang_P.forge_msg(lang, "stats", None, False, 8))
                        elif y[i] == "broken":
                            descDig += "{0} ".format(lang_P.forge_msg(lang, "stats", [y[i+1]], False, 19))
                        elif y[1] != "broken":
                            descDig += y[i] + " "
                        if i == len(y)-1:
                            descDig += ": `{0}`\n\n".format(x[0])

            elif x[1] == "slots":
                if x[2] == x[1]:
                    descSlots += "{2} **{1}** `{0}`\n\n".format(x[0], x[2], lang_P.forge_msg(lang, "stats", None, False, 15))
                else:
                    for i in range(1, len(y)):
                        if y[i] == "gain":
                            descSlots += "{0} ".format(lang_P.forge_msg(lang, "stats", None, False, 17))
                        elif y[i] == "perte":
                            descSlots += "{0} ".format(lang_P.forge_msg(lang, "stats", None, False, 18))
                        elif y[i] == "win":
                            descSlots += "{0} ".format(lang_P.forge_msg(lang, "stats", None, False, 30))
                        elif y[i] == "lose":
                            descSlots += "{0} ".format(lang_P.forge_msg(lang, "stats", None, False, 31))
                        else:
                            descSlots += y[i] + " "
                        if i == len(y)-1:
                            descSlots += ": `{0}`\n\n".format(x[0])

            elif x[1] == "boxes":
                if x[2] == x[1]:
                    descBoxes += "{2} **{1}** `{0}`\n\n".format(x[0], x[2], lang_P.forge_msg(lang, "stats", None, False, 15))
                else:
                    for i in range(1, len(y)):
                        if y[i] == "gain" and y[0] == "boxes":
                            descBoxes += "{0} ".format(lang_P.forge_msg(lang, "stats", None, False, 17))
                        elif y[i] == "gain" and y[0] == "lootbox":
                            descBoxes += "Lootbox {0}".format(y[1])
                        elif y[i] == "open":
                            descBoxes += "{0} ".format(lang_P.forge_msg(lang, "stats", None, False, 20))
                        elif y[0] != "lootbox":
                            descBoxes += y[i] + " "
                        if i == len(y)-1:
                            descBoxes += ": `{0}`\n\n".format(x[0])

            elif x[1] == "hothouse":
                if x[2] == x[1]:
                    descHothouse += "{2} **{1}** `{0}`\n\n".format(x[0], x[2], lang_P.forge_msg(lang, "stats", None, False, 15))
                else:
                    for i in range(1, len(y)):
                        if y[i] == "harvest":
                            descHothouse += "{1} {0} ".format(lang_P.forge_msg(lang, "stats", None, False, 25), y[3])
                        elif y[i] == "plant":
                            descHothouse += "{1} {0} ".format(lang_P.forge_msg(lang, "stats", None, False, 26), y[3])
                        if i == len(y)-1:
                            descHothouse += ": `{0}`\n\n".format(x[0])

            elif x[1] == "cooking":
                if x[2] == x[1]:
                    descCooking += "{2} **{1}** `{0}`\n\n".format(x[0], x[2], lang_P.forge_msg(lang, "stats", None, False, 15))
                else:
                    for i in range(1, len(y)):
                        if y[i] == "harvest":
                            descCooking += "{1} {0} ".format(lang_P.forge_msg(lang, "stats", None, False, 25), y[3])
                        elif y[i] == "plant":
                            descCooking += "{1} {0} ".format(lang_P.forge_msg(lang, "stats", None, False, 27), y[3])
                        if i == len(y)-1:
                            descCooking += ": `{0}`\n\n".format(x[0])

            elif x[1] == "ferment":
                if x[2] == x[1]:
                    descFerment += "{2} **{1}** `{0}`\n\n".format(x[0], x[2], lang_P.forge_msg(lang, "stats", None, False, 15))
                else:
                    for i in range(1, len(y)):
                        if y[i] == "harvest":
                            descFerment += "{1} {0} ".format(lang_P.forge_msg(lang, "stats", None, False, 25), y[3])
                        elif y[i] == "plant":
                            descFerment += "{1} {0} ".format(lang_P.forge_msg(lang, "stats", None, False, 28), y[3])
                        if i == len(y)-1:
                            descFerment += ": `{0}`\n\n".format(x[0])

            else:
                desc += "\n{1} `{0}`".format(x[0], x[2])

        msg = discord.Embed(title = "Statistiques de {0} | Gems Base".format(Nom), color= 13752280, description = "", timestamp=dt.datetime.now())
        msg.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
        # if descGeneral != "":
        #     msg.add_field(name=lang_P.forge_msg(lang, "stats", None, False, 0), value=descGeneral)
        if descBuy != "":
            msg.add_field(name=lang_P.forge_msg(lang, "stats", None, False, 1), value=descBuy)
        if descSell != "":
            msg.add_field(name=lang_P.forge_msg(lang, "stats", None, False, 2), value=descSell)
        if descDon != "":
            msg.add_field(name=lang_P.forge_msg(lang, "stats", None, False, 3), value=descDon)
        if descForge != "":
            msg.add_field(name=lang_P.forge_msg(lang, "stats", None, False, 4), value=descForge)
        if desc != "":
            msg.add_field(name=lang_P.forge_msg(lang, "stats", None, False, 14), value=desc)

        await ctx.channel.send(embed = msg)
        msg = discord.Embed(title = "Statistiques de {0} | Gems Play".format(Nom), color= 13752280, description = "", timestamp=dt.datetime.now())
        msg.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
        if descBank != "":
            msg.add_field(name=lang_P.forge_msg(lang, "stats", None, False, 5), value=descBank)
        if descMine != "":
            msg.add_field(name=lang_P.forge_msg(lang, "stats", None, False, 6), value=descMine)
        if descFish != "":
            msg.add_field(name=lang_P.forge_msg(lang, "stats", None, False, 7), value=descFish)
        if descDig != "":
            msg.add_field(name=lang_P.forge_msg(lang, "stats", None, False, 8), value=descDig)
        if descSlots != "":
            msg.add_field(name=lang_P.forge_msg(lang, "stats", None, False, 9), value=descSlots)
        if descBoxes != "":
            msg.add_field(name=lang_P.forge_msg(lang, "stats", None, False, 10), value=descBoxes)
        if descHothouse != "":
            msg.add_field(name=lang_P.forge_msg(lang, "stats", None, False, 11), value=descHothouse)
        if descCooking != "":
            msg.add_field(name=lang_P.forge_msg(lang, "stats", None, False, 12), value=descCooking)
        if descFerment != "":
            msg.add_field(name=lang_P.forge_msg(lang, "stats", None, False, 13), value=descFerment)

        await ctx.channel.send(embed = msg)

    @commands.command(pass_context=True)
    async def success(self, ctx):
        """
        Affiche la liste de tes succès
        """
        ID = ctx.author.id
        param = dict()
        param["ID"] = ID

        ge.socket.send_string(gg.std_send_command("success", ID, ge.name_pl, param))
        desc = GF.msg_recv()
        if desc[0] == "OK":
            lang = desc[1]
            msg = discord.Embed(title = lang_P.forge_msg(lang, "success", None, False, 0), color= 6824352, description = "", timestamp=dt.datetime.now())
            descS = desc[2]
            i = 0
            while i < len(descS):
                # print("Success >> {0} a obtenu le succes {1}".format(ctx.author.name, descS[i]))
                titre = descS[i]
                desc = descS[i+1]
                if i % 40 == 0 and i != 0:
                    msg.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
                    await ctx.channel.send(embed = msg)
                    msg = discord.Embed(title = lang_P.forge_msg(lang, "success", None, False, 0), color= 6824352, description = "", timestamp=dt.datetime.now())
                msg.add_field(name=titre, value=desc, inline=False)
                i += 2
            # msg.set_thumbnail(url=ctx.author.avatar_url)
            msg.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
            await ctx.channel.send(embed = msg)
        elif desc[0] == "Error":
            await ctx.channel.send(desc[2])
        else:
            await ctx.channel.send(desc[1])


def setup(bot):
    bot.add_cog(GemsSuccess(bot))
    open("help/cogs.txt", "a").write("GemsSuccess\n")
