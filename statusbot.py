import os
import time
from slackclient import SlackClient

from handlers import ConnectionError
from messages import parse_message, respond
from statuscheck import status

# Environment tokens
SLACK_TOKEN = os.environ.get("STATUSBOT_TOKEN")
BOT_NAME = os.environ.get("STATUSBOT_NAME")

if SLACK_TOKEN is None:
    raise EnvironmentError("STATUSBOT_TOKEN does not exist")
elif BOT_NAME is None:
    raise EnvironmentError("STATUSBOT_NAME does not exist")

# Client connection
client = SlackClient(SLACK_TOKEN)

BOT_ID = ""
apicall = client.api_call("users.list")
if apicall.get("ok"):
    users = apicall.get('members')
    for user in users:
        if user['name'] == BOT_NAME:
            BOT_ID = user['id']
else:
    raise ConnectionError("Could not connect to the Slack API! Check your connection and/or tokens.")

apicall = client.api_call("channels.list")
channels = []
if apicall.get("ok"):
    all_channels = apicall.get('channels')
    for chan in all_channels:
        if 'id' in chan.keys():
            channels.append(chan['id'])
else:
    raise ConnectionError("Could not connect to the Slack API! Check your connection and/or tokens.")


# Useful constants
AT_BOT = "<@" + BOT_ID + ">"
READ_WEBSOCKET_DELAY = 1

if client.rtm_connect():
    while True:
        message, channel = parse_message(client, channels, AT_BOT)
        if message is not None and channel is not None:
            respond(client, channel, status(message))
        time.sleep(READ_WEBSOCKET_DELAY)
else:
    raise ConnectionError("Could not connect to the Slakc API! Check your connection and/or tokens.")