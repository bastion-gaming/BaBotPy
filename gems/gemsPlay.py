import discord
from discord.ext import commands
from discord.ext.commands import bot
from gems import gemsFonctions as GF
from core import gestion as ge
import gg_lib as gg
from languages import lang as lang_P
import datetime as dt


class GemsPlay(commands.Cog):

    def __init__(self, ctx):
        return(None)

    @commands.command(pass_context=True)
    async def daily(self, ctx):
        """Récupère ta récompense journalière!"""
        # =======================================================================
        # Initialisation des variables générales de la fonction
        # =======================================================================
        ID = ctx.author.id
        param = dict()
        param["ID"] = ID
        ge.socket.send_string(gg.std_send_command("daily", ID, ge.name_pl, param))
        desc = GF.msg_recv()
        lang = desc[1]
        if desc[0] == "OK":
            msg = discord.Embed(title = lang_P.forge_msg(lang, "titres", None, False, 0), color= 13752280, description = desc[2])
            msg.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
            await ctx.channel.send(embed = msg)
        else:
            await ctx.channel.send(desc[2])

    @commands.command(pass_context=True)
    async def bank(self, ctx, ARG = None, ARG2 = None):
        """**[bal/add/saving] [nom/nombre]** | Compte épargne"""
        # =======================================================================
        # Initialistation des variables générales de la fonction
        # =======================================================================
        ID = ctx.author.id
        param = dict()
        param["ID"] = ID
        param["ARG"] = ARG
        param["ARG2"] = ARG2

        ge.socket.send_string(gg.std_send_command("bank", ID, ge.name_pl, param))
        desc = GF.msg_recv()
        lang = desc[1]
        if ARG == "bal" and ARG2 is not None:
            N = ctx.guild.get_member(ge.nom_ID(ARG2)).name
        else:
            N = ctx.author.name

        if desc[0] == "bal":
            if ARG2 != None:
                ID = ge.nom_ID(ARG2)
                nom = ctx.guild.get_member(ID)
                ARG2 = nom.name
                title = lang_P.forge_msg(lang, "bank", [N], False)
                # title = "Compte épargne de {}".format(ARG2)
            else:
                title = lang_P.forge_msg(lang, "bank", [N], False)
                # title = "Compte épargne de {}".format(ctx.author.name)
            msg = discord.Embed(title = title, color= 13752280, description = "", timestamp=dt.datetime.now())
            msg.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
            msg.add_field(name="Balance", value=desc[2], inline=False)
            msg.add_field(name="Commandes", value=desc[3], inline=False)
            await ctx.channel.send(embed = msg)

        elif desc[0] == "add":
            msg = discord.Embed(title = lang_P.forge_msg(lang, "titres", None, False, 4), color= 13752280, description = desc[2], timestamp=dt.datetime.now())
            msg.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
            await ctx.channel.send(embed = msg)

        elif desc[0] == "saving":
            msg = discord.Embed(title = lang_P.forge_msg(lang, "titres", None, False, 5), color= 13752280, description = desc[2], timestamp=dt.datetime.now())
            msg.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
            await ctx.channel.send(embed = msg)

        else:
            await ctx.channel.send(desc[2])

    @commands.command(pass_context=True)
    async def stealing(self, ctx, name=None):
        """*{nom}** | Vole des :gem:`gems` aux autres joueurs!"""
        ID = ctx.author.id
        param = dict()
        param["ID"] = ID
        param["name"] = name
        ge.socket.send_string(gg.std_send_command("stealing", ID, ge.name_pl, param))
        desc = GF.msg_recv()
        lang = desc[1]
        if desc[0] == "OK":
            msg = discord.Embed(title = lang_P.forge_msg(lang, "titres", None, False, 1), color= 13752280, description = desc[2])
            msg.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
            await ctx.channel.send(embed = msg)
        else:
            await ctx.channel.send(desc[2])

    @commands.command(pass_context=True)
    async def crime(self, ctx):
        """Commets un crime et gagne des :gem:`gems` Attention au DiscordCop!"""
        ID = ctx.author.id
        param = dict()
        param["ID"] = ID
        ge.socket.send_string(gg.std_send_command("crime", ID, ge.name_pl, param))
        desc = GF.msg_recv()
        lang = desc[1]
        if desc[0] == "OK":
            msg = discord.Embed(title = lang_P.forge_msg(lang, "titres", None, False, 2), color= 13752280, description = desc[2])
            msg.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
            await ctx.channel.send(embed = msg)
        else:
            await ctx.channel.send(desc[2])

    @commands.command(pass_context=True)
    async def gamble(self, ctx, valeur):
        """**[mise]** | Avez vous l'ame d'un parieur ?"""
        ID = ctx.author.id
        param = dict()
        param["ID"] = ID
        param["valeur"] = valeur
        ge.socket.send_string(gg.std_send_command("gamble", ID, ge.name_pl, param))
        desc = GF.msg_recv()
        lang = desc[1]
        if desc[0] == "OK":
            msg = discord.Embed(title = lang_P.forge_msg(lang, "titres", None, False, 3), color= 13752280, description = desc[2])
            msg.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
            await ctx.channel.send(embed = msg)
        else:
            await ctx.channel.send(desc[2])

    @commands.command(pass_context=True)
    async def mine(self, ctx):
        """Minez compagnons !!"""
        ID = ctx.author.id
        param = dict()
        param["ID"] = ID
        ge.socket.send_string(gg.std_send_command("mine", ID, ge.name_pl, param))
        desc = GF.msg_recv()
        lang = desc[1]
        if desc[0] == "OK":
            msg = discord.Embed(title = lang_P.forge_msg(lang, "stats", None, False, 6), color= 13752280, description = desc[2])
            msg.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
            await ctx.channel.send(embed = msg)
        else:
            await ctx.channel.send(desc[2])

    @commands.command(pass_context=True)
    async def dig(self, ctx):
        """Creusons compagnons !!"""
        ID = ctx.author.id
        param = dict()
        param["ID"] = ID
        ge.socket.send_string(gg.std_send_command("dig", ID, ge.name_pl, param))
        desc = GF.msg_recv()
        lang = desc[1]
        if desc[0] == "OK":
            msg = discord.Embed(title = lang_P.forge_msg(lang, "stats", None, False, 8), color= 13752280, description = desc[2])
            msg.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
            await ctx.channel.send(embed = msg)
        else:
            await ctx.channel.send(desc[2])

    @commands.command(pass_context=True)
    async def fish(self, ctx):
        """Péchons compagnons !!"""
        ID = ctx.author.id
        param = dict()
        param["ID"] = ID
        ge.socket.send_string(gg.std_send_command("fish", ID, ge.name_pl, param))
        desc = GF.msg_recv()
        lang = desc[1]
        if desc[0] == "OK":
            msg = discord.Embed(title = lang_P.forge_msg(lang, "stats", None, False, 7), color= 13752280, description = desc[2])
            msg.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
            await ctx.channel.send(embed = msg)
        else:
            await ctx.channel.send(desc[2])

    @commands.command(pass_context=True)
    async def slots(self, ctx, imise = None):
        """**{mise}** | La machine à sous, la mise minimum est de 10 :gem:`gems`"""
        ID = ctx.author.id
        param = dict()
        param["ID"] = ID
        param["imise"] = imise
        ge.socket.send_string(gg.std_send_command("slots", ID, ge.name_pl, param))
        desc = GF.msg_recv()
        lang = desc[1]
        if desc[0] == "OK":
            msg = discord.Embed(title = lang_P.forge_msg(lang, "stats", None, False, 9), color= 13752280, description = desc[2])
            msg.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
            await ctx.channel.send(embed = msg)
        else:
            await ctx.channel.send(desc[2])

    @commands.command(pass_context=True)
    async def open(self, ctx, name = None):
        """**[nom]** | Ouverture de Loot Box"""
        ID = ctx.author.id
        param = dict()
        param["ID"] = ID
        param["name"] = name
        ge.socket.send_string(gg.std_send_command("open", ID, ge.name_pl, param))
        msg = GF.msg_recv()

        if msg[0] == "OK":
            titre = msg[2]
            desc = msg[1]
            MsgEmbed = discord.Embed(title = "Loot Box | {}".format(titre), color= 13752280, description = desc)
            MsgEmbed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
            await ctx.channel.send(embed = MsgEmbed)
        else:
            await ctx.channel.send(msg[1])

    @commands.command(pass_context=True)
    async def hothouse(self, ctx, item = None):
        """**{seed/pumpkin}** | Plantons compagnons !!"""
        ID = ctx.author.id
        param = dict()
        param["ID"] = ID
        param["item"] = item
        ge.socket.send_string(gg.std_send_command("hothouse", ID, ge.name_pl, param))
        msg = GF.msg_recv()

        if msg[0] == "OK":
            lang = msg[1]
            nbplanting = msg[2]
            desc = lang_P.forge_msg(lang, "hothouse", [GF.get_idmoji("seed")], False, 0)
            titre = lang_P.forge_msg(lang, "hothouse", None, False, 1)
            MsgEmbed = discord.Embed(title = titre, color= 6466585, description = desc)
            k = len(msg)
            i = 3
            while i < k:
                j = (i-3)/2
                if j % 10 == 0 and j != nbplanting and j != 0:
                    if j // 10 == 1:
                        await ctx.channel.send(embed = MsgEmbed)
                    else:
                        await ctx.channel.send(embed = MsgEmbed, delete_after = 90)
                    MsgEmbed = discord.Embed(title = lang_P.forge_msg(lang, "hothouse", [int((j//10)+1)], False, 2), color= 6466585, description = "Voici tes plantation.")
                    MsgEmbed.add_field(name=lang_P.forge_msg(lang, "hothouse", [msg[i]], False, 3), value=msg[i+1], inline=False)
                else:
                    MsgEmbed.add_field(name=lang_P.forge_msg(lang, "hothouse", [msg[i]], False, 3), value=msg[i+1], inline=False)
                i += 2
            await ctx.channel.send(embed = MsgEmbed)
        else:
            await ctx.channel.send(msg[1])

    @commands.command(pass_context=True)
    async def ferment(self, ctx, item = None):
        """**{grapes/wheat}** | Cave de fermentation. Alcool illimité !!"""
        ID = ctx.author.id
        param = dict()
        param["ID"] = ID
        param["item"] = item
        ge.socket.send_string(gg.std_send_command("ferment", ID, ge.name_pl, param))
        msg = GF.msg_recv()

        if msg[0] == "OK":
            lang = msg[1]
            nbplanting = msg[2]
            desc = lang_P.forge_msg(lang, "ferment", None, False, 0)
            titre = lang_P.forge_msg(lang, "ferment", None, False, 1)
            MsgEmbed = discord.Embed(title = titre, color= 9633863, description = desc)
            k = len(msg)
            i = 3
            while i < k:
                j = (i-3)/2
                if j % 10 == 0 and j != nbplanting and j != 0:
                    if j // 10 == 1:
                        await ctx.channel.send(embed = MsgEmbed)
                    else:
                        await ctx.channel.send(embed = MsgEmbed, delete_after = 90)
                    MsgEmbed = discord.Embed(title = lang_P.forge_msg(lang, "ferment", [int((j//10)+1)], False, 2), color= 9633863, description = "Voici vos barrils.")
                    MsgEmbed.add_field(name=lang_P.forge_msg(lang, "ferment", [msg[i]], False, 3), value=msg[i+1], inline=False)
                else:
                    MsgEmbed.add_field(name=lang_P.forge_msg(lang, "ferment", [msg[i]], False, 3), value=msg[i+1], inline=False)
                i += 2
            await ctx.channel.send(embed = MsgEmbed)
        else:
            await ctx.channel.send(msg[1])

    @commands.command(pass_context=True)
    async def cooking(self, ctx, item = None):
        """**{potato/pumpkin/chocolate}** | Cuisinons compagnons !!"""
        ID = ctx.author.id
        param = dict()
        param["ID"] = ID
        param["item"] = item
        ge.socket.send_string(gg.std_send_command("cooking", ID, ge.name_pl, param))
        msg = GF.msg_recv()

        if msg[0] == "OK":
            lang = msg[1]
            nbplanting = msg[2]
            desc = lang_P.forge_msg(lang, "cooking", [GF.get_idmoji("fries")], False, 0)
            titre = lang_P.forge_msg(lang, "cooking", None, False, 1)
            MsgEmbed = discord.Embed(title = titre, color= 14902529, description = desc)
            k = len(msg)
            i = 3
            while i < k:
                j = (i-3)/2
                if j % 10 == 0 and j != nbplanting and j != 0:
                    if j // 10 == 1:
                        await ctx.channel.send(embed = MsgEmbed)
                    else:
                        await ctx.channel.send(embed = MsgEmbed, delete_after = 90)
                    MsgEmbed = discord.Embed(title = lang_P.forge_msg(lang, "cooking", [int((j//10)+1)], False, 2), color= 14902529, description = "Voici vos fours.")
                    MsgEmbed.add_field(name=lang_P.forge_msg(lang, "cooking", [msg[i]], False, 3), value=msg[i+1], inline=False)
                else:
                    MsgEmbed.add_field(name=lang_P.forge_msg(lang, "cooking", [msg[i]], False, 3), value=msg[i+1], inline=False)
                i += 2
            await ctx.channel.send(embed = MsgEmbed)
        else:
            await ctx.channel.send(msg[1])


def setup(bot):
    bot.add_cog(GemsPlay(bot))
    open("help/cogs.txt", "a").write("GemsPlay\n")
