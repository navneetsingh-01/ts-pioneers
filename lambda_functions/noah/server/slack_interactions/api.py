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
    message = f"{message}"
    data = {
        'channel': channel_id,
        'text': message,
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


def conversation_history(channel_id):
    logger.info("Checking conversation history for channel: " + str(channel_id))
    url = f"{base_url}/conversations.history"
    token = get_slack_token()
    headers = {
        'Authorization': f'Bearer {token}'
    }
    data = {
        'channel': channel_id
    }
    data = urllib.parse.urlencode(data).encode('utf-8')
    req = Request(url, data=data, headers=headers)
    try:
        response = urlopen(req)
        logger.info(response.read())
        return response
    except urllib.error.HTTPError as e:
        logger.info('Failed to send message. Error:', e.read().decode('utf-8'))
        return None
    except Exception as e:
        logger.info('Failed to send message. Error:', str(e))
        return None
