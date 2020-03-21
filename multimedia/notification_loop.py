import discord
from discord.ext import commands
from discord.ext.commands import Bot
import asyncio
import aiohttp
import json
import re
from datetime import datetime
from multimedia import notification as notif


PREFIX = open("core/prefix.txt", "r").read().replace("\n", "")
client = Bot(command_prefix = "{0}".format(PREFIX))

unresolved_ids = 0


############# Notification variables ################
TWITCH_CLIENT_ID = open("multimedia/twitch_client_id.txt", "r").read().replace("\n", "")
TWITCH_SECRET_ID = open("multimedia/twitch_secret_id.txt", "r").read().replace("\n", "")
unresolved_ids = 0

# Reset all sent key values to false
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

global counter
global first_startup
first_startup = 1


async def load(C):
    await asyncio.sleep(1)
    await looped_task(C)


# ---------------------------------------------------------------
# ---------------------------------------------------------------
# Task runs all the time, important to keep the asyncio.sleep at the end to avoid
# Function checks response from get_streams() and sends a message to joined discord channels accordingly.
async def looped_task(client):
    # await client.wait_until_ready()
    global api
    global first_startup
    global counter
    global users_url
    global token
    global users_response

    c_id = TWITCH_CLIENT_ID  # Client ID from Twitch Developers App
    c_secret = TWITCH_SECRET_ID  # Client Secret from Twitch Developers App

    # Loads json file containing information on channels and their subscribed streams as well as the last recorded
    # status of the streams

    # Check response from fecth() and messages discord channels
    if first_startup or unresolved_ids:
        users_url = await notif.make_users_url()
        await asyncio.sleep(2)

        # Fill in missing stream IDs from api to local JSON
        token = await notif.make_token(c_id, c_secret)  # Token to get twitch ID from all the added twitch usernames
        async with aiohttp.ClientSession() as session:
            users_response = await notif.get_users(token, session, users_url, 'json')
        await notif.fill_ids(users_response)

        await asyncio.sleep(2)  # Wait enough for login to print to console
        first_startup = 0
        await load(client)

    else:
        try:
            counter = counter + 1
        except:
            counter = 1
        live_counter = 0
        live_streams = []
        print("\n------\nCheck #{0}\nTime: {1}".format(counter, datetime.now()))

        streams_url = await notif.make_streams_url()
        async with aiohttp.ClientSession() as session:
            api = await notif.get_streams(c_id, session, streams_url, 'json')

        # Check for streams in local['streams'] that are not in any of the channels' subscriptions and remove those
        all_subscriptions = []
        for channel_index in local['channels']:
            for subscribed in channel_index['subscribed']:
                if subscribed not in all_subscriptions:
                    all_subscriptions.append(subscribed)

        for i, stream in enumerate(local['streams']):
            if stream['login'] not in all_subscriptions:
                # print('\nTime: ' + str(datetime.now()) + '\nAucun channel souscrit pour diffuser:\nSUPPRESSION: ' +
                #       stream['login'] + ' de local["streams"]\n')
                stream_list = local['streams']
                stream_list.pop(i)

                await notif.dump_json()

        # Check for streams in channel subscriptions that are not in the user_response
        for channel in local['channels']:
            channel_id = channel['id']
            for subscription in channel['subscribed']:
                exists = 0
                for user in users_response['data']:
                    if subscription == user['login']:
                        exists = 1

                if exists == 0:
                    sub_list = channel['subscribed']
                    sub_list.remove(subscription)

                    print('\nTime: ' + str(datetime.now()))
                    print("Le flux Twitch n'existe pas: ")
                    print('SUPPRESSION STREAM: ' + subscription + '\nCHANNEL ID: ' + str(channel_id))
                    msg = subscription + " n'existe pas, suppression du channel de la liste de notification."

                    channel_to_send = client.get_channel(channel_id)
                    await channel_to_send.send(msg)

                    await notif.dump_json()

        # Loop through api response and set offline stream's 'sent' key value to false
        # If stream is offline, set 'sent' key value to false, then save and reload the local JSON file
        for index in local['streams']:

            # print('\nSTREAM NAME: ' + index['login'])
            # print('STREAM ID: ' + index['id'])

            found_match = 0
            for api_index in api['data']:
                if api_index['user_id'] == index['id']:
                    # print("ID CORRESPONDANT DE L'API: " + api_index['user_id'])
                    found_match = 1
                    live_counter += 1
                    live_streams.append(index['login'])

            if found_match == 0:
                # print('ID CORRESPONDANT NON TROUVÉ')
                index['sent'] = 'false'
                index['status'] = 'offline'
                await notif.dump_json()

            else:
                index['status'] = 'live'

            # print('')

        streams_sent = []

        # Loop through channels and send out messages
        for channel in local['channels']:
            channel_id = channel['id']
            for subscribed_stream in channel['subscribed']:

                # Get correct id from local JSON
                for stream_index in local['streams']:
                    local_id = ''
                    if stream_index['login'] == subscribed_stream:
                        local_id = stream_index['id']

                    for api_index in api['data']:
                        if api_index['user_id'] == local_id:

                            status = api_index['type']

                            # If live, checks whether stream is live or vodcast, sets msg accordingly
                            # Sends message to channel, then saves sent status to json
                            if status == 'live' and stream_index['sent'] == 'false':
                                msg = "======= LIVE =======\n:regional_indicator_s: :regional_indicator_t: :regional_indicator_r: :regional_indicator_e: :regional_indicator_a: :regional_indicator_m:"

                                e = discord.Embed(title = api_index['title'], color= 9633863, description = "", url="https://www.twitch.tv/{0}".format(api_index['user_name']))
                                e.set_author(name=api_index['user_name'])# , icon_url=api_index['?'])
                                thumbnail_url = api_index['thumbnail_url'].replace("{width}", "480")
                                thumbnail_url = thumbnail_url.replace("{height}", "320")
                                # e.set_thumbnail(url=?)
                                e.set_image(url=thumbnail_url)
                                # e.add_field(name="Game", value=api_index['game_id'], inline=True)
                                e.add_field(name="Viewers", value=api_index['viewer_count'], inline=True)

                                channel_to_send = client.get_channel(channel_id)
                                try:
                                    await channel_to_send.send(msg)
                                    await channel_to_send.send(embed = e)
                                except:
                                    False

                            elif status == 'vodcast' and stream_index['sent'] == 'false':
                                msg = stream_index['login'] + ' VODCAST est en LIVE!\nhttps://www.twitch.tv/' + stream_index['login']
                                try:
                                    await client.send_message(client.get_channel(channel_id), msg)
                                except:
                                    False

                            # Loop through streams_sent[], if stream is not there, then add it
                            add_sent = 1
                            for stream in streams_sent:
                                if stream == stream_index['login']:
                                    add_sent = 0
                            if add_sent:
                                streams_sent.append(stream_index['login'])

        for login in local['streams']:
            for stream in streams_sent:
                if login['login'] == stream:
                    login['sent'] = 'true'

        await notif.dump_json()

        print('Live Channels: ' + str(live_counter))
        for stream in live_streams:
            print(stream)

        await asyncio.sleep(29)
        await load(client)
# ---------------------------------------------------------------
# ---------------------------------------------------------------