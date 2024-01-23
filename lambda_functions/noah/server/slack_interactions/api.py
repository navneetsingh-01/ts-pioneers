import os
import urllib
from ..logger import logger
from urllib.request import Request, urlopen

base_url = "https://slack.com/api"


def get_slack_token():
    return os.getenv("SLACK_BOT_TOKEN")


def slack_message(user, channel_id, message, ts):
    logger.info(
        f"Sending slack message.. User: {user}, Channel: {channel_id}, Timestamp: {ts}, Message: {message}")
    url = f"{base_url}/chat.postMessage"
    token = get_slack_token()
    message = f"<@{user}>\n{message}"
    data = {
        'channel': channel_id,
        'text': message,
        "thread_ts": ts,
        "mrkdwn": True
    }
    data = urllib.parse.urlencode(data).encode('utf-8')
    headers = {
        'Authorization': f'Bearer {token}'
    }
    req = Request(url, data=data, headers=headers)
    try:
        response = urlopen(req)
        logger.info('Message sent successfully!')
        return response
    except urllib.error.HTTPError as e:
        logger.info('Failed to send message. Error:', e.read().decode('utf-8'))
        return None
    except Exception as e:
        logger.info('Failed to send message. Error:', str(e))
        return None
