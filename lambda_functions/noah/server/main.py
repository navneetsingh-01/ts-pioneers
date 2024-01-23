import os
from .logger import logger
from .slack_interactions.api import slack_message, conversation_history


def event_handler(payload):
    logger.info("Event handler invoked")
    user = payload["event"]["user"]
    ts = payload["event"]["ts"]
    channel_id = payload["event"]["channel"]
    if 'bot_id' not in payload["event"]:
        slack_message(user, channel_id, "test message", ts)
    conversation_history('C06FPEGPRUY')
