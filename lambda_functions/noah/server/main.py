import os
from .logger import logger
from .slack_interactions.api import slack_message


def event_handler(payload):
    logger.info("Event handler invoked")
    user = payload["event"]["user"]
    ts = payload["event"]["ts"]
    channel_id = payload["event"]["channel"]
    slack_message(user, channel_id, "test message", ts)
