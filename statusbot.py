import os
import time
from slackclient import SlackClient

from handlers import ConnectionError

SLACK_TOKEN = os.environ.get("STATUSBOT_TOKEN")
BOT_NAME = os.environ.get("STATUSBOT_NAME")

if SLACK_TOKEN is None:
    raise EnvironmentError("STATUSBOT_TOKEN does not exist")
elif BOT_NAME is None:
    raise EnvironmentError("STATUSBOT_NAME does not exist")

client = SlackClient(SLACK_TOKEN)

bot_id = ""
apicall = client.api_call("users.list")
if apicall.get("ok"):
    users = apicall.get('members')
    for user in users:
        if user['name'] == BOT_NAME:
            bot_id = user['id']
else:
    raise ConnectionError("Could not connect to the Slack API")

