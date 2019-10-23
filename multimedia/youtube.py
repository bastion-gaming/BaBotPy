import os
import html
import googleapiclient.discovery
from core import welcome as wel

token_youtube = open("multimedia/token_youtube.txt","r").read().replace("\n","")

def search_youtube(user_input, number):
    # Disable OAuthlib's HTTPS verification when running locally.
    # *DO NOT* leave this option enabled in production.
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    api_service_name = "youtube"
    api_version = "v3"
    DEVELOPER_KEY = token_youtube

    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, developerKey=DEVELOPER_KEY)

    request = youtube.search().list(part="snippet",maxResults=number,q=user_input)
    response = request.execute()

    list = response["items"]

    out = []

    for l in list:
        title = html.unescape(l['snippet']['title'])
        try:
            if l['id']['kind'] == "youtube#channel":
                type = 'channel'
                id = l['id']['channelId']
            elif l['id']['kind'] == "youtube#playlist":
                type = 'playlist'
                id = l['id']['playlistId']
            elif l['id']['kind'] == "youtube#video":
                type = 'video'
                id = l['id']['videoId']
            else:
                type = 'unknown'
                id = "NoID"
        except KeyError:
            type = 'unknown'
            id = "NoID"

        out.append({'title': title, 'type': type, 'id': id})

    return out


def youtube_top_link(user_input):
    result = search_youtube(user_input, number=1)
    url = get_youtube_url(result[0])
    return result[0]['title'], url


def get_youtube_url(result):
    if result['type'] == 'video':
        url = "https://www.youtube.com/watch?v={}".format(result['id'])
    elif result['type'] == 'playlist':
        url = "https://www.youtube.com/playlist?list={}".format(result['id'])
    elif result['type'] == 'channel':
        url = "https://www.youtube.com/channel/{}".format(result['id'])
    else:
        url = None
    return url
