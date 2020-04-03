import discord
from core import gestion as ge
from gems import gemsFonctions as GF, gemsStats as GS
from discord.ext import commands
from discord.ext.commands import bot
import gg_lib as gg
import os
import datetime as dt
from languages import lang as lang_P

PREFIX = open("core/prefix.txt", "r").read().replace("\n", "")


class GemsBase(commands.Cog):

    def __init__(self, ctx):
        return(None)

    @commands.command(pass_context=True)
    async def tutorial(self, ctx, lang = "EN"):
        """Affiche le tutoriel !"""
        lang = lang.upper()
        langlist = ["EN", "FR"]
        if lang not in langlist:
            lang = "FR"
        desc = lang_P.forge_msg(lang, "tuto", None, False, 1)
        msg = discord.Embed(title = lang_P.forge_msg(lang, "tuto", None, False, 0), color= 13752280, description = desc)
        msg.add_field(name=lang_P.forge_msg(lang, "tuto", None, False, 2), value="https://get-gems.bastion-gaming.fr/tutorial", inline=False)
        await ctx.channel.send(embed = msg)

    @commands.command(pass_context=True)
    async def begin(self, ctx):
        """Pour créer son compte joueur et obtenir son starter Kit!"""
        ID = ctx.author.id
        param = dict()
        param["ID"] = ID
        param["name"] = ctx.author.name
        ge.socket.send_string(gg.std_send_command("begin", ID, ge.name_pl, param))
        msg = GF.msg_recv()
        await ctx.channel.send(msg[2])

    @commands.command(pass_context=True)
    async def connect(self, ctx, PlayerID):
        """**[PlayerID]** | WIP | Connecter un compte joueur d'une autre plateforme"""
        ID = ctx.author.id
        param = dict()
        param["ID"] = ID
        param["PlayerID"] = PlayerID
        ge.socket.send_string(gg.std_send_command("connect", ID, ge.name_pl, param))
        desc = GF.msg_recv()
        # if desc[0] == "OK":
        #     # A faire
        await ctx.channel.send(desc[2])

    @commands.command(pass_context=True)
    async def infos(self, ctx, nom = None):
        """**{name}** | Affiche les informations sur un joueur"""
        ID = ctx.author.id
        param = dict()
        if nom is None:
            nom = ctx.author.name
            param["ID"] = ID
            param["name"] = nom
        else:
            IDname = ge.nom_ID(nom)
            param["ID"] = IDname
            nom = ctx.guild.get_member(IDname)
            nom = nom.name
            param["name"] = nom
        ge.socket.send_string(gg.std_send_command("infos", ID, ge.name_pl, param))
        desc = GF.msg_recv()
        if desc[0] == "OK":
            lang = desc[1]
            title = lang_P.forge_msg(lang, "infos", [nom])
            msg = discord.Embed(title = title, color= 13752280, description = desc[2], timestamp=dt.datetime.now())
            msg.add_field(name="**_Balance_**", value=desc[3], inline=False)

            msg.add_field(name=desc[4], value=desc[5], inline=False)
            msg.add_field(name=desc[6], value=desc[7], inline=False)
            msg.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
            await ctx.channel.send(embed = msg)
            # Message de réussite dans la console
            print("Gems >> Informations de {0} affichée par {1}".format(nom, ctx.author.name))
            return
        else:
            await ctx.channel.send(desc[2])

    @commands.command(pass_context=True)
    async def bal(self, ctx, nom = None):
        """**{name}** | Êtes vous riche ou pauvre ?"""
        ID = ctx.author.id
        param = dict()
        param["fct"] = "None"
        if nom is None:
            nom = ctx.author.name
            param["ID"] = ID
        elif nom == "info":
            nom = ctx.author.name
            param["ID"] = ID
            param["fct"] = "info"
        else:
            IDname = ge.nom_ID(nom)
            param["ID"] = IDname
            nom = ctx.guild.get_member(IDname)
            nom = nom.name
        ge.socket.send_string(gg.std_send_command("bal", ID, ge.name_pl, param))
        desc = GF.msg_recv()
        if desc[0] == "OK":
            lang = desc[1]
            title = lang_P.forge_msg(lang, "bal", [nom], False)
            msg = discord.Embed(title = title, color= 13752280, description = "", timestamp=dt.datetime.now())
            msg.add_field(name="**_Balance_**", value=desc[2], inline=False)

            msg.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
            await ctx.channel.send(embed = msg)
            # Message de réussite dans la console
            print("Gems >> Balance de {} affichée".format(nom))
            return
        else:
            await ctx.channel.send(desc[2])

    @commands.command(pass_context=True)
    async def baltop(self, ctx, n = None, m = None):
        """**{filtre} {nombre}** | Classement des joueurs"""
        ID = ctx.author.id
        param = dict()
        param["ID"] = ID
        try:
            if n == None:
                n = 10
            else:
                n = int(n)
            filtre = "gems"
        except:
            if m == None:
                filtre = n
                n = 10
            else:
                filtre = n
                n = int(m)
        filtre = filtre.lower()
        param["nb"] = n
        param["filtre"] = filtre
        ge.socket.send_string(gg.std_send_command("baltop", ID, ge.name_pl, param))
        desc = GF.msg_recv()

        if desc[0] == "OK":
            lang = desc[1]
            if filtre == "gems" or filtre == "gem" or filtre == "spinelles" or filtre == "spinelle":
                Titre = lang_P.forge_msg(lang, "baltop", None, False, 0)
                if filtre == "spinelles" or filtre == "spinelle":
                    Titre = lang_P.forge_msg(lang, "baltop", [GF.get_idmoji("spinelle")], False, 1)

                msg = discord.Embed(title = Titre, color= 13752280, description = desc[2])
                # Message de réussite dans la console
                print("Gems >> {} a afficher le classement des {} premiers joueurs | Filtre: {}".format(ctx.author.name, n, filtre))

            elif filtre == "guild" or filtre == "guilde":
                Titre = lang_P.forge_msg(lang, "baltop", None, False, 2)
                msg = discord.Embed(title = Titre, color= 13752280, description = desc[2])
                # Message de réussite dans la console
                print("Gems >> {} a afficher le classement des {} premières guildes".format(ctx.author.name, n))

            else:
                msg = discord.Embed(title = "Classement", color= 13752280, description = "Erreur! Commande incorrect")
            await ctx.channel.send(embed = msg)
        else:
            await ctx.channel.send(desc[2])

    @commands.command(pass_context=True)
    async def buy(self, ctx, item, nb = 1):
        """**[item] {nombre}** | Permet d'acheter les items vendus au marché"""
        ID = ctx.author.id
        param = dict()
        param["ID"] = ID
        # param["IDGuild"] = ctx.guild.id
        param["nb"] = nb
        param["item"] = item

        ge.socket.send_string(gg.std_send_command("buy", ID, ge.name_pl, param))
        desc = GF.msg_recv()
        lang = desc[1]
        if desc[0] == "OK":
            msg = discord.Embed(title = lang_P.forge_msg(lang, "stats", None, False, 1), color= 13752280, description = desc[2])
            msg.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
            await ctx.channel.send(embed = msg)
        else:
            await ctx.channel.send(desc[2])

    @commands.command(pass_context=True)
    async def sell(self, ctx, item, nb = 1):
        """**[item] {nombre}** | Permet de vendre vos items !"""
        ID = ctx.author.id
        param = dict()
        param["ID"] = ID
        # param["IDGuild"] = ctx.guild.id
        param["nb"] = nb
        param["item"] = item

        ge.socket.send_string(gg.std_send_command("sell", ID, ge.name_pl, param))
        desc = GF.msg_recv()
        lang = desc[1]
        if desc[0] == "OK":
            msg = discord.Embed(title = lang_P.forge_msg(lang, "stats", None, False, 2), color= 13752280, description = desc[2])
            msg.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
            await ctx.channel.send(embed = msg)
        else:
            await ctx.channel.send(desc[2])

    @commands.command(pass_context=True)
    async def inv(self, ctx, fct = None):
        """**{nom de la poche}** | Permet de voir ce que vous avez dans le ventre !"""
        ID = ctx.author.id
        nom = ctx.author.name
        param = dict()
        param["ID"] = ID
        # param["IDGuild"] = ctx.guild.id
        if fct is not None:
            fct = fct.lower()
        param["fct"] = fct

        ge.socket.send_string(gg.std_send_command("inv", ID, ge.name_pl, param))
        desc = GF.msg_recv()

        if desc[0] == "OK":
            lang = desc[1]
            msg_titre = lang_P.forge_msg(lang, "inv", [nom], False, 0)
            msg = discord.Embed(title = msg_titre, color= 6466585, description = desc[2])
            if desc[3] != "None":
                msg.add_field(name=lang_P.forge_msg(lang, "categorie", None, False, 0), value=desc[3], inline=False)
            if desc[4] != "None":
                msg.add_field(name=lang_P.forge_msg(lang, "categorie", None, False, 1), value=desc[4], inline=False)
            if desc[5] != "None":
                msg.add_field(name=lang_P.forge_msg(lang, "categorie", None, False, 2), value=desc[5], inline=False)
            if desc[6] != "None":
                msg.add_field(name=lang_P.forge_msg(lang, "categorie", None, False, 3), value=desc[6], inline=False)
            if desc[7] != "None":
                msg.add_field(name=lang_P.forge_msg(lang, "categorie", None, False, 4), value=desc[7], inline=False)
            if desc[8] != "None":
                msg.add_field(name=lang_P.forge_msg(lang, "categorie", None, False, 5), value=desc[8], inline=False)
            if desc[9] != "None":
                msg.add_field(name=lang_P.forge_msg(lang, "categorie", None, False, 6), value=desc[9], inline=False)
            if desc[10] != "None":
                msg.add_field(name=lang_P.forge_msg(lang, "categorie", None, False, 7), value=desc[10], inline=False)
            await ctx.channel.send(embed = msg)

        elif desc[0] == "pockets":
            lang = desc[1]
            msg = discord.Embed(title = lang_P.forge_msg(lang, "inv", None, False, 1), color= 6466585, description = desc[2], timestamp=dt.datetime.now())
            msg.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
            await ctx.channel.send(embed = msg)

        else:
            await ctx.channel.send(desc[2])

    @commands.command(pass_context=True)
    async def market(self, ctx, fct = None):
        """**{stand}** | Permet de voir tout les objets que l'on peux acheter ou vendre !"""
        ID = ctx.author.id
        param = dict()
        param["ID"] = ID
        # param["IDGuild"] = ctx.guild.id
        if fct is not None:
            fct = fct.lower()
        param["fct"] = fct

        ge.socket.send_string(gg.std_send_command("market", ID, ge.name_pl, param))
        desc = GF.msg_recv()

        if desc[0] == "OK":
            lang = desc[1]
            if fct != None:
                msg = discord.Embed(title = lang_P.forge_msg(lang, "market", [fct], False, 1), color= 2461129, description = desc[2], timestamp=dt.datetime.now())
            else:
                msg = discord.Embed(title = lang_P.forge_msg(lang, "market", None, False, 0), color= 2461129, description = desc[2], timestamp=dt.datetime.now())
            msg.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
            if fct == "mobile":
                msg.add_field(name=lang_P.forge_msg(lang, "categorie", None, False, 0), value=desc[3], inline=False)
                msg.add_field(name=lang_P.forge_msg(lang, "categorie", None, False, 1), value=desc[4], inline=False)
                msg.add_field(name=lang_P.forge_msg(lang, "categorie", None, False, 3), value=desc[5], inline=False)
                msg.add_field(name=lang_P.forge_msg(lang, "categorie", None, False, 4), value=desc[6], inline=False)
                msg.add_field(name=lang_P.forge_msg(lang, "categorie", None, False, 5), value=desc[7], inline=False)
                if desc[7] != "None":
                    msg.add_field(name=lang_P.forge_msg(lang, "categorie", None, False, 2), value=desc[8], inline=False)
                if desc[8] != "None":
                    msg.add_field(name=lang_P.forge_msg(lang, "categorie", None, False, 6), value=desc[9], inline=False)
                if desc[9] != "None":
                    msg.add_field(name="Spinelles <:spinelle:{}>".format(GF.get_idmoji("spinelle")), value=desc[10], inline=False)

                msg.add_field(name=lang_P.forge_msg(lang, "categorie", None, False, 7), value=desc[11], inline=False)
                await ctx.channel.send(embed = msg)

            else:
                if fct == None or fct == "outil" or fct == "outils":
                    msg.add_field(name=lang_P.forge_msg(lang, "categorie", None, False, 0), value=desc[4], inline=True)
                    msg.add_field(name=lang_P.forge_msg(lang, "market", None, False, 2), value=desc[5], inline=True)
                    msg.add_field(name=lang_P.forge_msg(lang, "market", None, False, 4), value=desc[6], inline=True)

                if fct == None or fct == "outils" or fct == "outil" or fct == "item" or fct == "items" or fct == "minerai" or fct == "minerais" or fct == "poissons" or fct == "fish" or fct == "plantes" or fct == "plants" or fct == "event" or fct == "événements":
                    if desc[6] != "None":
                        msg.add_field(name=lang_P.forge_msg(lang, "categorie", None, False, 1), value=desc[7], inline=True)
                        msg.add_field(name=lang_P.forge_msg(lang, "market", None, False, 2), value=desc[8], inline=True)
                        msg.add_field(name=lang_P.forge_msg(lang, "market", None, False, 4), value=desc[9], inline=True)

                if fct == None or fct == "minerai" or fct == "minerais":
                    msg.add_field(name=lang_P.forge_msg(lang, "categorie", None, False, 3), value=desc[10], inline=True)
                    msg.add_field(name=lang_P.forge_msg(lang, "market", None, False, 2), value=desc[11], inline=True)
                    msg.add_field(name=lang_P.forge_msg(lang, "market", None, False, 4), value=desc[12], inline=True)

                if fct == None or fct == "fish" or fct == "poissons":
                    msg.add_field(name=lang_P.forge_msg(lang, "categorie", None, False, 4), value=desc[13], inline=True)
                    msg.add_field(name=lang_P.forge_msg(lang, "market", None, False, 2), value=desc[14], inline=True)
                    msg.add_field(name=lang_P.forge_msg(lang, "market", None, False, 4), value=desc[15], inline=True)

                if fct == None or fct == "plants" or fct == "plantes":
                    msg.add_field(name=lang_P.forge_msg(lang, "categorie", None, False, 5), value=desc[16], inline=True)
                    msg.add_field(name=lang_P.forge_msg(lang, "market", None, False, 2), value=desc[17], inline=True)
                    msg.add_field(name=lang_P.forge_msg(lang, "market", None, False, 4), value=desc[18], inline=True)

                if fct == None or fct == "item" or fct == "items":
                    msg.add_field(name=lang_P.forge_msg(lang, "categorie", None, False, 2), value=desc[19], inline=True)
                    msg.add_field(name=lang_P.forge_msg(lang, "market", None, False, 2), value=desc[20], inline=True)
                    msg.add_field(name=lang_P.forge_msg(lang, "market", None, False, 4), value=desc[21], inline=True)

                if fct == None or fct == "event" or fct == "événements":
                    msg.add_field(name=lang_P.forge_msg(lang, "categorie", None, False, 6), value=desc[22], inline=True)
                    msg.add_field(name=lang_P.forge_msg(lang, "market", None, False, 2), value=desc[23], inline=True)
                    msg.add_field(name=lang_P.forge_msg(lang, "market", None, False, 4), value=desc[24], inline=True)

                if fct == None or fct == "lootbox":
                    msg.add_field(name=lang_P.forge_msg(lang, "categorie", None, False, 7), value=desc[25], inline=True)
                    msg.add_field(name=lang_P.forge_msg(lang, "market", None, False, 3), value=desc[26], inline=True)
                    msg.add_field(name=lang_P.forge_msg(lang, "market", None, False, 5), value=desc[27], inline=True)
                await ctx.channel.send(embed = msg)

        else:
            await ctx.channel.send(desc[2])

    @commands.command(pass_context=True)
    async def pay(self, ctx, nom, gain):
        """**[nom] [gain]** | Donner de l'argent à vos amis !"""
        ID = ctx.author.id
        param = dict()
        param["ID"] = ID
        # param["IDGuild"] = ctx.guild.id
        param["nom"] = ctx.author.name
        param["ID_recu"] = ge.nom_ID(nom)
        param["Nom_recu"] = ctx.guild.get_member(param["ID_recu"]).name
        param["gain"] = gain

        ge.socket.send_string(gg.std_send_command("pay", ID, ge.name_pl, param))
        desc = GF.msg_recv()
        lang = desc[1]
        if desc[0] == "OK":
            msg = discord.Embed(title = lang_P.forge_msg(lang, "stats", None, False, 3), color= 13752280, description = desc[2])
            msg.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
            await ctx.channel.send(embed = msg)
        else:
            await ctx.channel.send(desc[2])

    @commands.command(pass_context=True)
    async def give(self, ctx, nom, item, nb = None):
        """**[nom] [item] [nombre]** | Donner des items à vos amis !"""
        ID = ctx.author.id
        param = dict()
        param["ID"] = ID
        # param["IDGuild"] = ctx.guild.id
        param["nom"] = ctx.author.name
        param["ID_recu"] = ge.nom_ID(nom)
        param["Nom_recu"] = ctx.guild.get_member(param["ID_recu"]).name
        param["item"] = item
        param["nb"] = nb

        ge.socket.send_string(gg.std_send_command("give", ID, ge.name_pl, param))
        desc = GF.msg_recv()
        lang = desc[1]
        if desc[0] == "OK":
            msg = discord.Embed(title = lang_P.forge_msg(lang, "stats", None, False, 3), color= 13752280, description = desc[2])
            msg.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
            await ctx.channel.send(embed = msg)
        else:
            await ctx.channel.send(desc[2])

    @commands.command(pass_context=True)
    async def forge(self, ctx, item = None, nb = 1):
        """**{item} {nombre}** | Permet de concevoir des items spécifiques"""
        ID = ctx.author.id
        param = dict()
        param["ID"] = ID
        # param["IDGuild"] = ctx.guild.id
        param["item"] = item
        param["nb"] = nb

        ge.socket.send_string(gg.std_send_command("forge", ID, ge.name_pl, param))
        desc = GF.msg_recv()
        lang = desc[1]
        if desc[0] == "OK":
            if item == None:
                msg = discord.Embed(title = lang_P.forge_msg(lang, "recette"), color= 15778560, description = desc[2])
                await ctx.channel.send(embed = msg)
            else:
                msg = discord.Embed(title = lang_P.forge_msg(lang, "stats", None, False, 4), color= 13752280, description = desc[2])
                msg.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
                await ctx.channel.send(embed = msg)
        else:
            await ctx.channel.send(desc[2])

    @commands.command(pass_context=True)
    async def graphbourse(self, ctx, item, moisD = None, anneeD = None, moisF = None, anneeF = None, type = None):
        """**[item] {mois début} {année début} {mois fin} {année fin}** | Historique de la bourse par item"""
        ID = ctx.author.id
        now = dt.datetime.now()

        if item.lower() == "all":
            if anneeF is not None:
                temp = type
            type = moisD.lower()
            if anneeD is None:
                anneeD = str(now.year)
                moisD = str(now.month)
            else:
                moisD = anneeD
                anneeD = moisF
            if anneeF is None:
                moisF = str(now.month)
                anneeF = str(now.year)
            else:
                moisF = anneeF
                anneeF = temp
            param = dict()
            param["ID"] = ID
            param["type"] = type

            ge.socket.send_string(gg.std_send_command("listobjet", ID, ge.name_pl, param))
            msg = GF.msg_recv()

            if msg[0] == "NOK":
                await ctx.channel.send(msg[1])
            else:
                for one in msg[1]:
                    graph = GS.create_graphbourse(ctx, one, anneeD, moisD, anneeF, moisF)
                    lang = graph[1]
                    if graph[0] == "404":
                        await ctx.send(lang_P.forge_msg(lang, "WarningMsg", None, False, 0))
                    else:
                        await ctx.send(file=discord.File("cache/{}".format(graph[0])))
                        os.remove("cache/{}".format(graph[0]))
        else:
            if moisD == None:
                moisD = str(now.month)
            if anneeD == None:
                anneeD = str(now.year)
            if moisF == None:
                moisF = str(now.month)
            if anneeF == None:
                anneeF = str(now.year)
            graph = GS.create_graphbourse(ctx, item, anneeD, moisD, anneeF, moisF)
            lang = graph[1]
            if graph[0] == "404":
                await ctx.send(lang_P.forge_msg(lang, "WarningMsg", None, False, 0))
            else:
                await ctx.send(file=discord.File("cache/{}".format(graph[0])))
                os.remove("cache/{}".format(graph[0]))

    @commands.command(pass_context=True)
    async def lang(self, ctx, langue = None):
        """**{langue}** | Permet de changer la langue pour un joueur."""
        ID = ctx.author.id
        param = dict()
        param["ID"] = ID
        param["langue"] = langue

        ge.socket.send_string(gg.std_send_command("lang", ID, ge.name_pl, param))
        desc = GF.msg_recv()

        await ctx.channel.send(desc[1])

    @commands.command(pass_context=True)
    async def godparent(self, ctx, nom):
        """**[name]** | Permet d'ajouter un joueur comme parrain."""
        ID = ctx.author.id
        param = dict()
        param["ID"] = ID
        param["GPID"] = ge.nom_ID(nom)
        ge.socket.send_string(gg.std_send_command("godparent", ID, ge.name_pl, param))
        desc = GF.msg_recv()
        lang = desc[1]
        if ID == ge.nom_ID(nom):
            await ctx.channel.send(lang_P.forge_msg(lang, "godparent"))
        else:
            await ctx.channel.send(desc[2])

    # ==============================
    # ===== Commande désactivé =====
    # ==============================
    # @commands.command(pass_context=True)
    # async def convert(self, ctx, nb = None):
    #     """**[Nombre de spinelle]** | Convertisseur :gem:`gems` :left_right_arrow: `spinelles` (250 000 pour 1)"""
    #     ID = ctx.author.id
    #     param = dict()
    #     param["ID"] = ID
    #     param["IDGuild"] = ctx.guild.id
    #     param["nb"] = nb
    #
    #     ge.socket.send_string(gg.std_send_command("convert", ID, ge.name_pl, param))
    #     desc = GF.msg_recv()
    #
    #     await ctx.channel.send(desc[1])


def setup(bot):
    bot.add_cog(GemsBase(bot))
    open("help/cogs.txt", "a").write("GemsBase\n")
