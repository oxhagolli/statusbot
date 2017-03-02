import platform
import os


def status(message):
    host = message[0]
    if host == "localhost" or host == "127.0.0.1":
        return "Don't even try ..."
    host = host.replace('<', '').replace('>', '')
    if len(host.split("|")) > 1:
        host = host.split("|")[1]
    query = "ping {} {}".format(
        '-n 1' if platform.system().lower() == "windows" else '-c 1',
        host
    )
    print(query)
    response = "{} is {}.".format(host, "up" if os.system(query) == 0 else "down or does not exist.")
    return response
