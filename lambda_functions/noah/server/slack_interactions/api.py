import os
import urllib
import json
import html
import requests
from ..logger import logger
from urllib.request import Request, urlopen

base_url = "https://slack.com/api"


def get_slack_token():
    return os.getenv("SLACK_BOT_TOKEN")


def slack_message(user, channel_id, message):
    logger.info(
        f"Sending slack message.. User: {user}, Channel: {channel_id}, Message: {message}")
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


def slack_location_message(channel_id, message):
    print(
        f"Sending slack message... Channel: {channel_id}, Message: {message}")
    url = f"{base_url}/chat.postMessage"
    token = get_slack_token()
    message = f"{message}"
    data = {
        'channel': channel_id,
        'text': message,
        'thread_ts': "1704364326.321319",
        "mrkdwn": True,
        "blocks": [
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": message
                }
            },
            {
                "type": "actions",
                "elements": [
                    {
                        "type": "button",
                        "text": {
                            "type": "plain_text",
                            "text": "Home"
                        },
                        "style": "primary",
                        "value": "app"
                    },
                    {
                        "type": "button",
                        "text": {
                            "type": "plain_text",
                            "text": "Office"
                        },
                        "style": "primary",
                        "value": "app"
                    }
                ]
            }
        ]
    }
    data = urllib.parse.urlencode(data).encode('utf-8')
    headers = {
        'Authorization': f'Bearer {token}'
    }

    try:
        req = Request(url, data=data, headers=headers)
        response = urlopen(req)
        result = json.loads(response.read().decode('utf-8'))
        logger.info(result)
        logger.info(type(result))
        logger.info('Message sent successfully!')
        return response
    except urllib.error.HTTPError as e:
        logger.info('Failed to send message. Error:', e.read().decode('utf-8'))
        return None
    except Exception as e:
        logger.info('Failed to send message. Error:', str(e))
        return None


def slack_ad_link_btn(channel_id, message):
    print(
        f"Sending slack message... Channel: {channel_id}, Message: {message}")
    url = f"{base_url}/chat.postMessage"
    token = get_slack_token()
    message = f"{message}"
    data = {
        'channel': channel_id,
        'text': message,
        'thread_ts': "1704364326.321319",
        "mrkdwn": True,
        "blocks": [
            {
                "type": "section",
                        "text": {
                            "type": "mrkdwn",
                            "text": "Okay, I got it. Click the following button to reset your password"
                        },
                "accessory": {
                            "type": "button",
                            "text": {
                                    "type": "plain_text",
                                "text": "Password Reset",
                            },
                            "value": "click_me_123",
                            "url": "https://sfdcpwd.internal.salesforce.com/RDWeb/Pages/en-US/password.aspx",
                        }
            }
        ]
    }
    data = urllib.parse.urlencode(data).encode('utf-8')
    headers = {
        'Authorization': f'Bearer {token}'
    }

    try:
        req = Request(url, data=data, headers=headers)
        response = urlopen(req)
        result = json.loads(response.read().decode('utf-8'))
        print(result)
        print(type(result))
        print('Message sent successfully!')
        return response
    except urllib.error.HTTPError as e:
        print('Failed to send message. Error:', e.read().decode('utf-8'))
        return None
    except Exception as e:
        print('Failed to send message. Error:', str(e))
        return None


def slack_log_case(channel_id, message):
    print(
        f"Sending slack message... Channel: {channel_id}, Message: {message}")
    url = f"{base_url}/chat.postMessage"
    token = get_slack_token()
    message = f"{message}"
    data = {
        'channel': channel_id,
        'text': message,
        'thread_ts': "1704364326.321319",
        "mrkdwn": True,
        "blocks": [
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "Do you wish to log a case for your issue?"
                }
            },
            {
                "type": "actions",
                "elements": [
                    {
                        "type": "button",
                        "text": {
                            "type": "plain_text",
                            "text": "Yes"
                        },
                        "style": "primary",
                        "value": "click_me_123"
                    },
                    {
                        "type": "button",
                        "text": {
                            "type": "plain_text",
                            "text": "No"
                        },
                        "style": "danger",
                        "value": "click_me_123"
                    }
                ]
            }
        ]
    }
    data = urllib.parse.urlencode(data).encode('utf-8')
    headers = {
        'Authorization': f'Bearer {token}'
    }

    try:
        req = Request(url, data=data, headers=headers)
        response = urlopen(req)
        result = json.loads(response.read().decode('utf-8'))
        logger.info(result)
        logger.info(type(result))
        logger.info('Message sent successfully!')
        return response
    except urllib.error.HTTPError as e:
        logger.info('Failed to send message. Error:', e.read().decode('utf-8'))
        return None
    except Exception as e:
        logger.info('Failed to send message. Error:', str(e))
        return None


def conversation_history_ai(channel_id, applicationReffered):
    print("Checking conversation history for channel: " + str(channel_id))
    url = f"{base_url}/conversations.history"
    # Make sure you have a function named get_slack_token that returns your Slack token
    token = get_slack_token()

    headers = {
        'Authorization': f'Bearer {token}'
    }

    params = {
        'channel': channel_id,
        'limit': 5,
    }

    response = requests.get(url, headers=headers, params=params)
    try:
        logger.info(response.json())
        conversation_history = response.json()["messages"]
        for message in conversation_history:
            if "client_msg_id" in message.keys():
                to_parse = message["text"]
            prompt = f"From the text presented to you, extract what applications will be down and present in a json as such: resposnePresent: true/false,systemsDown:<list of ssystems>, if there is no such information in the text then mark responsePresent as false else mark it as true the input text is: {to_parse}"
            url = "https://supportforce--spf24hack.sandbox.my.salesforce.com/services/data/v58.0/einstein/llm/prompt/generations"
            headers = {
                'Authorization': 'Bearer 00DO2000000nLP8!AQEAQNFQNO_Q6f4NLWf4T401dFMm1THl6iejczOnIGUI3lezlzcpZFhuDsugZmCZ.nezJ_cQztOf3F9diRFA.NiiWrSgWCs0',
                'Content-Type': 'application/json'
            }

            data = {
                "promptTextorId": prompt,
                "provider": "OpenAI",
                "additionalConfig": {"maxTokens": 512, "applicationName": "BillingInquiry"}
            }
            response = requests.post(url, headers=headers, json=data)
            responseString = response.json()["generations"][0]["text"]

            decoded_json = html.unescape(responseString)

# Parse the JSON string
            parsed_json = json.loads(decoded_json)
            logger.info(parsed_json)
            response = parsed_json
            if parsed_json["responsePresent"] == True:
                if applicationReffered in (parsed_json["systemsDown"]):
                    logger.info("Outage detected")

        logger.info("{} messages found in {}".format(
            len(conversation_history), channel_id))
        return response
    except urllib.error.HTTPError as e:
        logger.info('Failed to send message. Error:', e.read().decode('utf-8'))
        return None
    except Exception as e:
        logger.info('Failed to send message. Error:', str(e))
        return None


def slack_reset_ad(channel_id, message):
    print(
        f"Sending slack message... Channel: {channel_id}, Message: {message}")
    url = f"{base_url}/chat.postMessage"
    token = get_slack_token()
    message = f"{message}"
    data = {
        'channel': channel_id,
        'text': message,
        'thread_ts': "1704364326.321319",
        "mrkdwn": True,
        "blocks": [
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "Is your AD Password reset?"
                }
            },
            {
                "type": "actions",
                "elements": [
                    {
                        "type": "button",
                        "text": {
                            "type": "plain_text",
                            "text": "Yes"
                        },
                        "style": "primary",
                        "value": "ADPASSWORD"
                    },
                    {
                        "type": "button",
                        "text": {
                            "type": "plain_text",
                            "text": "No"
                        },
                        "style": "danger",
                        "value": "click_me_123"
                    }
                ]
            }
        ]
    }
    data = urllib.parse.urlencode(data).encode('utf-8')
    headers = {
        'Authorization': f'Bearer {token}'
    }

    try:
        req = Request(url, data=data, headers=headers)
        response = urlopen(req)
        result = json.loads(response.read().decode('utf-8'))
        logger.info(result)
        logger.info(type(result))
        logger.info('Message sent successfully!')
        return response
    except urllib.error.HTTPError as e:
        logger.info('Failed to send message. Error:', e.read().decode('utf-8'))
        return None
    except Exception as e:
        logger.info('Failed to send message. Error:', str(e))
        return None


def slack_forget_password(channel_id, message):
    print(
        f"Sending slack message... Channel: {channel_id}, Message: {message}")
    url = f"{base_url}/chat.postMessage"
    token = get_slack_token()
    message = f"{message}"
    data = {
        'channel': channel_id,
        'text': message,
        'thread_ts': "1704364326.321319",
        "mrkdwn": True,
        "blocks": [
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "Do you remember your current password?"
                }
            },
            {
                "type": "actions",
                "elements": [
                    {
                        "type": "button",
                        "text": {
                            "type": "plain_text",
                            "text": "Yes"
                        },
                        "style": "primary",
                        "value": "FORGETPASSWORD"
                    },
                    {
                        "type": "button",
                        "text": {
                            "type": "plain_text",
                            "text": "No"
                        },
                        "style": "danger",
                        "value": "click_me_123"
                    }
                ]
            }
        ]
    }
    data = urllib.parse.urlencode(data).encode('utf-8')
    headers = {
        'Authorization': f'Bearer {token}'
    }

    try:
        req = Request(url, data=data, headers=headers)
        response = urlopen(req)
        result = json.loads(response.read().decode('utf-8'))
        print(result)
        print(type(result))
        print('Message sent successfully!')
        return response
    except urllib.error.HTTPError as e:
        print('Failed to send message. Error:', e.read().decode('utf-8'))
        return None
    except Exception as e:
        print('Failed to send message. Error:', str(e))
        return None
