import discord
from discord.ext import commands, tasks
from discord.ext.commands import Bot
from discord.utils import get
import datetime as t
from datetime import datetime
import DB
import roles
import stats as stat
import notification as notif
import asyncio
import aiohttp
import json
import re

# initialisation des variables.
DEFAUT_PREFIX = "!"

VERSION = open("fichier_txt/version.txt").read().replace("\n","")
TOKEN = open("fichier_txt/token.txt", "r").read().replace("\n","")
PREFIX = open("fichier_txt/prefix.txt","r").read().replace("\n","")
client = commands.Bot(command_prefix = "{0}".format(PREFIX))
NONE = open("fichier_txt/cogs.txt","w")
NONE = open("fichier_txt/help.txt","w")

############# Notification variables ################
TWITCH_CLIENT_ID = open("fichier_txt/twitch_client_id.txt", "r").read().replace("\n","")
TWITCH_SECRET_ID = open("fichier_txt/twitch_secret_id.txt", "r").read().replace("\n","")
unresolved_ids = 0
# Reset all sent key values to false
with open('fichier_json/local.json', 'r') as fp:
	reset_values = json.load(fp)
for streams_index in reset_values['streams']:
	streams_index['sent'] = 'false'
with open('fichier_json/local.json', 'w') as fp:
	json.dump(reset_values, fp, indent=2)


with open('fichier_json/local.json', 'r') as fp:
	local = json.load(fp)

with open('fichier_json/userlist.json', 'r') as fp:
	user_list = json.load(fp)

api = {}
#####################################################

client.remove_command("help")

# Au démarrage du Bot.
@client.event
async def on_ready():
	print('Connecté avec le nom : {0.user}'.format(client))
	print('PREFIX = '+str(PREFIX))
	print('\nBastionBot '+VERSION)
	if DB.dbExist():
		print("La DB "+ DB.DB_NOM +" existe, poursuite sans soucis.")
	else :
		print("La DB n'existait pas. Elle a été (re)créée.")
	flag = DB.checkField()
	if flag == 0:
		print("Aucun champ n'a été ajouté ni supprimé no modifié.")
	elif "add" in flag:
		print("Un ou plusieurs champs ont été ajoutés à la DB.")
	elif "sup" in flag:
		print("Un ou plusieurs champs ont été supprimés de la DB.")
	elif "type" in flag:
		print("Un ou plusieurs type ont été modifié sur la DB.")


	print('| Core Module | >> Connecté !')

####################### Commande help.py #######################

client.load_extension('help')

################### Core ############################

client.load_extension('utils')

################### Welcome #################################

@client.event
async def on_member_join(member):
	await roles.autorole(member)
	channel = client.get_channel(417445503110742048)
	time = t.time()
	#data = sqlite3.connect('connect.db')
	#c = data.cursor()
	id = member.id
	if DB.newPlayer(id) == "Le joueur a été ajouté !":
		msg = ":black_small_square:Bienvenue {0} sur Bastion!:black_small_square: \n\n\nNous sommes ravis que tu aies rejoint notre communauté ! \nTu es attendu : \n\n:arrow_right: Sur #⌈:closed_book:⌋•règles \n:arrow_right: Sur #⌈:ledger:⌋•liste-salons\n\n=====================".format(member.mention)
	else:
		msg = "=====================\nBon retour parmis nous ! {0}\n\n=====================".format(member.mention)
	stat.countCo()
	await channel.send(msg)

@client.event
async def on_member_remove(member):
	stat.countDeco()
	channel = client.get_channel(417445503110742048)
	await channel.send("{0} nous a quitté, pourtant si jeune...".format(member.mention))

####################### Stat ####################################

@client.event
async def on_message(message):
	if not (message.author.bot or message.content.startswith(PREFIX)) :
		await stat.countMsg(message)
		await client.process_commands(message)
	else:
		await client.process_commands(message)

####################### Commande stats.py #######################

client.load_extension('stats')

####################### Commande roles.py #######################

client.load_extension('roles')

###################### Commande gestion.py #####################

client.load_extension('gestion')

####################### Commande gems.py #######################

client.load_extension('gems')

###################### Commande notification.py ################

client.load_extension('notification')

#---------------------------------------------------------------
#---------------------------------------------------------------
# Task runs all the time, important to keep the asyncio.sleep at the end to avoid
# Function checks response from get_streams() and sends a message to joined discord channels accordingly.
async def looped_task():
	await client.wait_until_ready()
	global api

	c_id = TWITCH_CLIENT_ID  # Client ID from Twitch Developers App
	c_secret = TWITCH_SECRET_ID  # Client Secret from Twitch Developers App

	# Loads json file containing information on channels and their subscribed streams as well as the last recorded
	# status of the streams
	counter = 0  # Counter mostly for debug
	first_startup = 1  # Prepwork

	# Check response from fecth() and messages discord channels
	while not client.is_closed():
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

		else:
			counter += 1
			live_counter = 0
			live_streams = []
			print('\n------\nCheck #' + str(counter) + '\nTime: ' + str(datetime.now()))

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
					print('\nTime: ' + str(datetime.now()) + '\nAucun channel souscrit pour diffuser:\nSUPPRESSION: ' +
						  stream['login'] + ' de local["streams"]\n')
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

				print('\nSTREAM NAME: ' + index['login'])
				print('STREAM ID: ' + index['id'])

				found_match = 0
				for api_index in api['data']:
					if api_index['user_id'] == index['id']:
						print("ID CORRESPONDANT DE L'API: " + api_index['user_id'])
						found_match = 1
						live_counter += 1
						live_streams.append(index['login'])

				if found_match == 0:
					print('ID CORRESPONDANT NON TROUVÉ')
					index['sent'] = 'false'
					index['status'] = 'offline'
					await notif.dump_json()

				else:
					index['status'] = 'live'

				print('')

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
								if status == 'live' and stream_index['sent'] == 'false' and stream_index['login'] != "bastionlivetv":
									msg = "======= LIVE =======\n:regional_indicator_s: :regional_indicator_t: :regional_indicator_r: :regional_indicator_e: :regional_indicator_a: :regional_indicator_m:\n\n{0} est en live !!!\nAllez voir -> https://www.twitch.tv/{0}".format(stream_index['login'])

									channel_to_send = client.get_channel(channel_id)
									await channel_to_send.send(msg)

								elif status == 'live' and stream_index['sent'] == 'false' and stream_index['login'] == "bastionlivetv":
									msg = "======= LIVE =======\n:regional_indicator_s: :regional_indicator_t: :regional_indicator_r: :regional_indicator_e: :regional_indicator_a: :regional_indicator_m:\n\nNous sommes en live sur BastionLiveTv !\nRegardez nous ici : https://www.twitch.tv/{0}\nPour voir les dates => http://www.bastion-gaming.fr/agenda.html".format(stream_index['login'])

									channel_to_send = client.get_channel(channel_id)
									await channel_to_send.send(msg)

								elif status == 'vodcast' and stream_index['sent'] == 'false':
									msg = stream_index['login'] + ' VODCAST est en LIVE!\nhttps://www.twitch.tv/' + stream_index['login']
									await client.send_message(client.get_channel(channel_id), msg)

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

			await asyncio.sleep(30)  # task runs every x second(s)
#---------------------------------------------------------------
#---------------------------------------------------------------

###################### Commande vocal.py ########################

client.load_extension('vocal')

##################### Commande kaamelott.py #####################

client.load_extension('kaamelott')

####################### Lancemement du bot ######################


client.loop.create_task(looped_task())
client.run(TOKEN)
