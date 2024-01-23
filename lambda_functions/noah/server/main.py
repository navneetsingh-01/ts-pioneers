import os
from .logger import logger
from .slack_interactions.api import slack_message, conversation_history
from .supportforce_interactions.api import log_case


def event_handler(payload):
    logger.info("Event handler invoked")
    user = payload["event"]["user"]
    ts = payload["event"]["ts"]
    channel_id = payload["event"]["channel"]
    if 'bot_id' in payload["event"]:
        logger.info("Message sent by the BOT")
        return
    slack_message(user, channel_id, "test message", ts)
    conversation_history(os.getenv("INCIDENTS_CHANNEL"))
    log_case()
