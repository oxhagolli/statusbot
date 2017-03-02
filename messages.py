from slackclient import SlackClient


def parse_message(client, public_channels, AT_BOT):
    assert type(client) == SlackClient
    e = client.rtm_read()
    message = None
    channel = None
    for obj in e:
        if obj['type'] == 'message' and 'bot_id' not in obj.keys():
            if 'text' in obj.keys() and AT_BOT in obj['text']:
                message = obj['text'].split()[1:]
                channel = obj['channel']
            elif 'text' in obj.keys() and obj['channel'] not in public_channels:
                message = obj['text'].split()
                channel = obj['channel']
    return message, channel


def respond(client, channel, message):
    assert client is not None
    assert channel is not None
    client.api_call("chat.postMessage",
                    channel=channel,
                    text=message,
                    as_user=True)
