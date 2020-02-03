import discord
from discord.ext import commands
from discord.ext.commands import Bot
import aiohttp
import json
import re


PREFIX = open("core/prefix.txt", "r").read().replace("\n", "")
client = Bot(command_prefix = "{0}".format(PREFIX))

unresolved_ids = 0

# Réinitialiser toutes les valeurs de clé envoyées sur false
with open('multimedia/local.json', 'r') as fp:
    reset_values = json.load(fp)
for streams_index in reset_values['streams']:
    streams_index['sent'] = 'false'
with open('multimedia/local.json', 'w') as fp:
    json.dump(reset_values, fp, indent=2)


with open('multimedia/local.json', 'r') as fp:
    local = json.load(fp)

with open('multimedia/userlist.json', 'r') as fp:
    user_list = json.load(fp)

api = {}


async def dump_json():
    with open('multimedia/local.json' , 'w') as fp:
        json.dump(local, fp, indent=2)

    with open('multimedia/userlist.json' , 'w') as fp:
        json.dump(user_list, fp, indent=2)


# Retourne la réponse de twitch api
async def get_streams(c_id, session, url, response_type):
    # Param qui contient l'ID client
    headers = {
        'Client-ID': '{}'.format(c_id)
    }

    # Obtient et retourne la réponse de twitch api, en utilisant l'en-tête défini ci-dessus.
    async with session.get(url, headers=headers, timeout=10) as response:
        if response_type == 'text':
            return await response.text()
        elif response_type == 'json':
            return await response.json()


# Retourne la réponse de twitch api
async def get_users(token, session, url, response_type):

    # Param qui contient l'ID client
    headers = {
        'Authorization': 'Bearer {}'.format(token)
    }

    # Obtient et retourne la réponse de twitch api, en utilisant l'en-tête défini ci-dessus.
    async with session.get(url, headers=headers, timeout=10) as response:
        if response_type == 'text':
            return await response.text()
        elif response_type == 'json':
            return await response.json()


async def make_token(client_id, client_secret):
    print('\nObtention du token TWITCH...')
    token_url = 'https://id.twitch.tv/oauth2/token?client_id={}&client_secret={}&grant_type=client_credentials'.format(
        client_id, client_secret)
    async with aiohttp.ClientSession() as session:
        async with session.post(token_url) as response:
            response = await response.json()
            token = response['access_token']
            print('Token: ' + token + '\n------')
            return token


# Créer et renvoyer l'URL de l'API des flux Twitch avec les user_logins dans local.json
async def make_streams_url():
    streams = local['streams']

    url = 'https://api.twitch.tv/helix/streams?user_login='

    for index, login in enumerate(streams):
        if index == 0:
            url = url + login['login']
        else:
            url = url + '&user_login=' + login['login']

    return url


# Créer et renvoyer l'URL de l'API des flux Twitch avec les user_logins dans local.json
async def make_users_url():
    stream = local['streams']

    url = 'https://api.twitch.tv/helix/users?login='

    for index, login in enumerate(stream):
        if index == 0:
            url = url + login['login']
        else:
            url = url + '&login=' + login['login']

    return url


async def fill_ids(users_response):
    global unresolved_ids
    counter = 0

    print('\nRemplir les identifiants manquants ...')
    for local_user in local['streams']:
        if local_user['id'] == "":
            for user in users_response['data']:
                if local_user['login'] == user['login']:
                    counter += 1
                    print("ID manquant rempli pour l'utilisateur: " + local_user['login'] + " : " + user['id'])
                    local_user['id'] = user['id']

    if counter == 0:
        print('Aucun identifiant manquant.')
    else:
        print('\n' + str(counter) + ' ID remplis.')

    unresolved_ids = 0
    await dump_json()


class Notification(commands.Cog):

    def __init__(self, ctx):
        return(None)

    @commands.command(pass_context=True)
    async def notif_list(self, ctx):
        """Affiche la liste des notifications"""
        channel_id = ctx.message.channel.id
        channel_exists = 0
        has_subscriptions = 0

        # print('\n------\n\nTime: ' + str(datetime.now()))
        # print('Demande de liste du channel' + str(channel_id))

        msg = 'Vous recevez actuellement des notifications pour les channels suivants:\n'
        for channel in local['channels']:

            # Vérifiez si le channel a été ajouté à local.json
            if channel['id'] == channel_id:
                channel_exists = 1
                for stream in channel['subscribed']:
                    has_subscriptions = 1
                    msg = msg + '\n' + stream

        # Si le channel n'existe pas, envoyez un message à ctx et retournez
        if channel_exists == 0:
            msg = "Ce channel discord n'a pas encore été vérifié."
            # print("Impossible de supprimer le flux, le channel n'a pas été ajouté au bot.\n------\n")
            await ctx.channel.send(msg)
            return

        elif not has_subscriptions:
            msg = "Vous n'avez ajouté aucun twitch channels."
            # print('Aucun abonnement ajouté.\n------\n')
            await ctx.channel.send(msg)
            return

        else:
            # print('\n------\n')
            await ctx.channel.send(msg)

    @commands.command(pass_context=True)
    async def checklive(self, ctx):
        """Affiche le nombre de flux en direct"""
        c_id = ctx.message.channel.id
        streams_live = []

        for channel in local['channels']:
            if c_id == channel['id']:
                if len(channel['subscribed']) == 0:
                    msg = "Vous n'avez ajouté aucun twitch channels."
                    await ctx.channel.send(msg)
                    return

        for stream in local['streams']:
            if stream['status'] == 'live':
                streams_live.append(stream['login'])

        if len(streams_live) == 1:
            msg = 'Depuis vos notifications, il y a actuellement 1 flux en direct:\n\n'
            for login in streams_live:
                msg = msg + '{}\n'.format(login)

        elif len(streams_live) > 0:
            msg = 'Depuis vos notifications, il y a actuellement {} flux en direct:\n\n'.format(len(streams_live))
            for login in streams_live:
                msg = msg + '{}\n'.format(login)

        else:
            msg = "Il n'y a pas de flux en direct."

        await ctx.channel.send(msg)

    @commands.command(pass_context=True)
    async def removestream(self, ctx, arg):
        """Permet de retirer un flux des notifications"""
        channel_id = ctx.message.channel.id
        channel_exists = 0
        arg = str(arg.lower())

        # print('\n------\n\nTime: ' + str(datetime.now()))
        # print('Remove request from channel ' + str(channel_id) + ' for stream name ' + arg)

        # Vérifiez si le channel a été ajouté à local.json
        for channel in local['channels']:
            if channel['id'] == channel_id:
                channel_exists = 1

        # Si le channel n'existe pas, envoyez un message à ctx et retournez
        if channel_exists == 0:
            msg = "Ce channel discord n'a pas encore été vérifié."
            # print("Impossible de supprimer le flux, le channel n'a pas été ajouté au bot.")
            await ctx.channel.send(msg)
            return

        if not re.match('^[a-zA-Z0-9_]+$', arg):
            msg = 'Le nom ne doit pas contenir de caractères spéciaux.'
            # print(msg)
            await ctx.channel.send(msg)
            return

        # Vérifiez la liste des chaînes dans local.json pour éviter les doublons.
        for i, channel in enumerate(local['channels']):
            subscription_exists = 0

            if channel['id'] == channel_id:
                for stream in channel['subscribed']:
                    if stream == arg:
                        subscription_exists = 1

                if subscription_exists:
                    subscriptions = channel['subscribed']
                    subscriptions.remove(arg)
                    await dump_json()

                    # print('\nENLEVÉ: \nSTREAM: ' + arg + '\nCHANNEL ID: ' + str(channel_id) + '\n------\n')

                    msg = 'Enlevé ' + arg + '.'
                    await ctx.channel.send(msg)

                else:
                    # print(arg + " n'existe pas dans les abonnements aux chaînes")

                    msg = arg + " n'est pas actuellement dans vos notifications."
                    await ctx.channel.send(msg)

    @commands.command(pass_context=True)
    async def addstream(self, ctx, arg):
        """Ajouter un flux twitch aux notifications de channel"""
        global unresolved_ids
        channel_id = ctx.message.channel.id
        stream_exists = 0
        channel_exists = 0
        subscription_exists = 0
        arg = str(arg.lower())
        new_stream = {
            "login": arg,
            "sent": "false",
            "id": "",
            "status": ""
        }

        # print('\n------\n\nTime: ' + str(datetime.now()))
        # print('Ajouter une demande du channel ' + str(channel_id) + ' pour le flux ' + arg)

        if not re.match('^[a-zA-Z0-9_]+$', arg):
            msg = 'Le nom ne doit pas contenir de caractères spéciaux.'
            # print(msg)
            await ctx.channel.send(msg)
            return

        # Vérifiez la liste des flux dans local.json pour éviter les doublons
        for index in local['streams']:
            if index['login'] == arg:
                stream_exists = 1

        # Vérifiez la liste des chaînes dans local.json pour éviter les doublons.
        for channel in local['channels']:

            # Vérifiez si le channel a été ajouté à local.json
            if channel['id'] == channel_id:
                channel_exists = 1

                for stream in channel['subscribed']:

                    # Vérifier si le flux est déjà dans les abonnements de la chaîne
                    if stream == arg:
                        subscription_exists = 1

        # Si le channel n'existe pas, envoyez un message à ctx et retournez
        if channel_exists == 0:
            msg = "Ce channel discord n'a pas encore été vérifié."
            # print("Impossible d'ajouter le flux, le channel n'a pas été ajouté au bot.")
            await ctx.channel.send(msg)
            return

        # Agit sur les contrôles ci-dessus
        if subscription_exists == 0 and stream_exists == 0:
            local.setdefault('streams', []).append(new_stream)
            unresolved_ids = 1

            for channel in local['channels']:
                if channel['id'] == channel_id:
                    change = channel['subscribed']
                    change.append(arg)

            await dump_json()

            # print('\nAJOUTÉ: \nSTREAM: ' + arg + '\nCHANNEL ID: ' + str(channel_id) + '\nAJOUTÉ AUX FLUX\n------\n')

            msg = arg + ' a été ajouté à vos notifications.'
            await ctx.channel.send(msg)

        elif subscription_exists == 1 and stream_exists == 0:
            local.setdefault('streams', []).append(new_stream)
            unresolved_ids = 1

            await dump_json()

            # print('\nAJOUTÉ AUX FLUX\n------\n')

            msg = arg + ' est déjà dans vos notifications.'
            await ctx.channel.send(msg)

        elif subscription_exists == 0 and stream_exists == 1:
            for channel in local['channels']:
                if channel['id'] == channel_id:
                    change = channel['subscribed']
                    change.append(arg)

            # print('\nAJOUTÉ: \nSTREAM: ' + arg + '\nCHANNEL ID: ' + str(channel_id) + '\n------\n')

            await dump_json()

            msg = 'Ajouté ' + arg + ' to your notifications.'
            await ctx.channel.send(msg)

        elif subscription_exists == 1 and stream_exists == 1:
            # print('DÉJÀ AJOUTÉ')
            msg = arg + ' a déjà été ajouté à vos notifications!'
            await ctx.channel.send(msg)

    @commands.command(pass_context=True)
    async def addchannel(self, ctx):
        """Ajouter un channel au bot"""
        s_name = ctx.message.guild.name
        c_name = ctx.message.channel.name
        c_id = ctx.message.channel.id
        u_id = ctx.message.author.id
        u_name = ctx.message.author.name

        verified = 0
        duplicate = 0
        # print('\n------\n\nTime: ' + str(datetime.now()))
        # print("Requete d'ajout de channel pour:\nSERVER: {}\nCHANNEL: {} avec l'ID {}"
        #       "\nUSER: {} avec l'ID {}".format(s_name, c_name, c_id, u_name, u_id))

        # Vérifier si l'utilisateur est autorisé à ajouter des channels
        for id in user_list['verified_users']:
            if u_id == id:
                verified = 1

        # Si l'utilisateur peut être vérifié, recherchez les doublons, puis ajoutez le channel
        if verified:

            # Vérifier les ID de channel en double
            for channel in local['channels']:
                if channel['id'] == c_id:
                    duplicate = 1

            # Act on duplicate check
            if not duplicate:
                new_channel = {
                    "id": c_id,
                    "guild_name": s_name,
                    "channel_name": c_name,
                    "added_by_name": u_name,
                    "added_by_id": u_id,
                    "subscribed": []
                }

                local['channels'].append(new_channel)
                await dump_json()

                msg = 'Channel ajouté!'
                # print(msg + '\n------\n')
                await ctx.channel.send(msg)

            else:
                msg = 'Ce channel a déjà été ajouté!'
                # print(msg + '\n------\n')
                await ctx.channel.send(msg)

        else:
            # print("L'utilisateur n'est pas autorisé à ajouter des channels.\n------\n")
            msg = "Vous n'êtes pas autorisé à ajouter des channels."
            await ctx.channel.send(msg)

    @commands.command(pass_context=True)
    async def removechannel(self, ctx):
        """Supprimer le channel du bot"""
        c_id = ctx.message.channel.id
        u_id = ctx.message.author.id

        verified = 0
        channel_exists = 0

        # print('\n------\n\nTime: ' + str(datetime.now()))
        # print("Requete de suppression de channel pour:\nSERVER: {}\nCHANNEL: {} avec l'ID {}"
        #       "\nUSER: {} avec l'ID {}".format(s_name, c_name, c_id, u_name, u_id))

        # Check if user is allowed to add channels
        for id in user_list['verified_users']:
            if u_id == id:
                verified = 1

        # If user can be verified, try remove channel with correct id
        if verified:
            channel_list = local['channels']
            for channel in channel_list:
                if channel['id'] == c_id:
                    channel_exists = 1
                    channel_list.remove(channel)
                    await dump_json()

            if channel_exists:
                msg = 'Channel supprimé!'
                # print(msg + '\n------\n')
                await ctx.channel.send(msg)

            else:
                msg = "Le channel a déjà été supprimée ou n'a jamais été ajoutée."
                # print(msg + '\n------\n')
                await ctx.channel.send(msg)

        else:
            # print("L'utilisateur n'est pas autorisé à supprimer des channels.\n------\n")
            msg = "Vous n'êtes pas autorisé à supprimer des channels."
            await ctx.channel.send(msg)

    @commands.command(pass_context=True)
    async def adduser(self, ctx, arg):
        """Ajouter un utilisateur à la liste vérifiée. Cela ne peut être fait que par des utilisateurs maîtres."""
        u_id = ctx.message.author.id

        # print('\n------\n\nTime: ' + str(datetime.now()))
        # print('Verify User request from:\nSERVER: {}\nCHANNEL: {} with ID {}'
        #       '\nUSER: {} with ID {}\nFor user ID: {}'.format(s_name, c_name, c_id, u_name, u_id, arg))

        # Check if user is master user
        if u_id not in user_list['master_users']:
            msg = 'You are not authorized to add users.'
            # print('User is not a master user.')
            await ctx.channel.send(msg)
            return

        # Make the argument into an int
        try:
            arg = int(arg)
        except ValueError:
            # print('Request cancelled, invalid argument.\n------\n')
            await ctx.channel.send("That didn't work, please try again.")
            return

        # If user is not already verified, add it
        if arg not in user_list['verified_users']:
            user_list['verified_users'].append(arg)
            await dump_json()

            msg = 'User ID {} is now verified.'.format(str(arg))
            # print(msg + '\n------\n')
            await ctx.channel.send(msg)

        else:
            msg = 'User ID {} is already verified.'.format(str(arg))
            # print(msg + '\n------\n')
            await ctx.channel.send(msg)

    @commands.command(pass_context=True)
    async def removeuser(self, ctx, arg):
        """Supprimer un utilisateur de la liste vérifiée. Cela ne peut être fait que par des utilisateurs maîtres."""
        u_id = ctx.message.author.id

        # print('\n------\n\nTime: ' + str(datetime.now()))
        # print('Remove Verified User request from:\nSERVER: {}\nCHANNEL: {} with ID {}'
        #       '\nUSER: {} with ID {}\nFor user ID: {}'.format(s_name, c_name, c_id, u_name, u_id, arg))

        # Check if user is master user
        if u_id not in user_list['master_users']:
            msg = 'You are not authorized to remove users.'
            # print('User is not a master user.')
            await ctx.channel.send(msg)
            return

        # Make the argument into an int
        try:
            arg = int(arg)
        except ValueError:
            # print('Request cancelled, invalid argument.\n------\n')
            await ctx.channel.send("That didn't work, please try again.")
            return

        list = user_list['verified_users']
        try:
            list.remove(arg)
            await dump_json()

            msg = 'Removed user ID {} from verified users.'.format(str(arg))
            # print(msg + '\n------\n')
            await ctx.channel.send(msg)

        except ValueError:
            msg = 'User ID {} is not a verified user.'.format(str(arg))
            # print(msg + '\n------\n')
            await ctx.channel.send(msg)


def setup(bot):
    bot.add_cog(Notification(bot))
    open("help/cogs.txt", "a").write("Notification\n")
