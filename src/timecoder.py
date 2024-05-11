import json
from datetime import datetime
from urllib.request import urlopen, Request


# YOUTUBE_API_KEY = 'YOUR_API_KEY'
# YOUTUBE_CHANNEL_ID = 'UCRM04HMvn5PAfAyyqNIpaIQ'
# YOUTUBE_LAST_STREAM_URL = f'https://www.googleapis.com/youtube/v3/search?key={YOUTUBE_API_KEY}&channelId={YOUTUBE_CHANNEL_ID}&part=snippet,id&order=date&maxResults=1'

# TWITCH_CLIENT_ID = 'YOUR_CLIENT_ID'
# TWITCH_OAUTH_TOKEN = 'YOUR_OAUTH_TOKEN'
# TWITCH_STREAMS_URL = f'https://api.twitch.tv/helix/streams?user_login={TWITCH_CHANNEL_NAME}'
# TWITCH_HEADERS = {
#     'Client-ID': TWITCH_CLIENT_ID,
#     'Authorization': f'Bearer {TWITCH_OAUTH_TOKEN}'
# }

STREAMERSONGLIST_STREAMER_URL_TPL = 'https://api.streamersonglist.com/v1/streamers/{}?platform=twitch&isUsername=true'
STREAMERSONGLIST_HISTORY_TPL = 'https://api.streamersonglist.com/v1/streamers/{}/playHistory?size=99&type=playedAt&order=desc&period=week'
TIME_LIMIT_IN_SECONDS = 1 * 60 * 60


def get_response_data(url):
    try:
        with urlopen(url) as response:
            return json.loads(response.read())
    except Exception as error:
        print(
            f"Couldn't get response for HTTP GET request.\n"
                f"URL: {url}\n"
                f"Error: {str(error)}"
        )


# def get_last_youtube_stream_date():
#     data = get_response_data(YOUTUBE_LAST_STREAM_URL)
#     if data is None:
#         return
#     if 'items' not in data:
#         return
#     if not len(data['items']):
#         return
#
#     return datetime.fromisoformat(data['items'][0]['snippet']['publishedAt'])


# def get_last_twitch_stream_date():
#     data = get_response_data(Request(TWITCH_STREAMS_URL, headers=TWITCH_HEADERS))
#     if data is None:
#         return
#     if 'data' not in data:
#         return
#     if not len(data['data']):
#         return
#
#     return datetime.fromisoformat(data['data'][0]['started_at'])


def format_item(item):
    if 'song' in item:
        return f"00:00:00 {item['song']['artist'].strip()} - {item['song']['title'].strip()}"
    elif 'nonlistSong' in item:
        return f"00:00:00 {item['nonlistSong'].strip()}"
    else:
        print(
            f"Warning. Couldn't generate a timecode for the song.\n"
            f"item: {item}"
        )


def take_last_stream_played(items):
    if len(items) == 0:
        return

    for i in range(len(items) - 1):
        yield items[i]

        played_at1 = datetime.fromisoformat(items[i]['playedAt'])
        played_at2 = datetime.fromisoformat(items[i + 1]['playedAt'])

        if (played_at1 - played_at2).total_seconds() > TIME_LIMIT_IN_SECONDS:
            break
    else:
        yield items[-1]


def main():
    # last_youtube_stream_date = get_last_youtube_stream_date()
    # if last_youtube_stream_date is None:
    #     print("The YouTube channel has no streams or an error occurred")
    #     exit(1)
    #
    # print(f"The last stream on YouTube was published at {last_youtube_stream_date}")
    # exit(0)

    # last_twitch_stream_date = get_last_twitch_stream_date()
    # if last_twitch_stream_date is None:
    #     print("The channel has no streams or an error occurred")
    #     exit(1)
    #
    # print(f"The last stream on Twitch was published at {last_twitch_stream_date}")
    # exit(0)

    if len(sys.argv) > 1:
        twitch_channel_name = sys.argv[1]
    else:
        twitch_channel_name = os.environ.get('TWITCH_CHANNEL_NAME', 'ALISAMAGRO')

    twitch_channel_name = twitch_channel_name.lower()

    streamer = get_response_data(
        STREAMERSONGLIST_STREAMER_URL_TPL.format(twitch_channel_name))
    if streamer is None:
        exit(1)

    history = get_response_data(STREAMERSONGLIST_HISTORY_TPL.format(streamer['id']))
    if history is None:
        exit(1)

    print('\n'.join(
        reversed(list(
            map(format_item, take_last_stream_played(history['items']))
        ))
    ))

    input("Press Enter to exit...")


if __name__ == '__main__':
    main()
