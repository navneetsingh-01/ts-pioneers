import os
import requests
import threading
import time
from .logger import logger
from .slack_interactions.api import slack_message, conversation_history, slack_location_message, slack_log_case, conversation_history_ai
from .supportforce_interactions.api import log_case
from .utils import getApplicationError, check_internet_speed


def event_handler(payload):
    if 'bot_id' in payload["event"]:
        logger.info("Message sent by the BOT")
        return

    logger.info("Event handler invoked")
    user = payload["event"]["user"]
    channel_id = payload["event"]["channel"]
    message = payload["event"]["text"]

    # application = getApplicationError(message)
    # logger.info(str(application) + type(application))

    application = message

    if 'gmeet' in str(application).lower() or 'network' in str(application).lower() or 'google' in str(application).lower():
        app = 'Google Meet'
        if 'network' in str(application).lower():
            app = 'Internet'
        slack_message(
            user, channel_id, "I understand you are having issues with your " + app)
        slack_location_message(channel_id, "Please specify your location", app)

    else:
        slack_message(user, channel_id,
                      "I can't handle this request. Look out for future updates :)")

    conversation_history(os.getenv("INCIDENTS_CHANNEL"))
    # log_case()


def handle_interactive_response(payload):
    if payload.lower().count("home") == 2:
        logger.info("Home option selected")
        slack_message("U05FJ0V6QBZ", "D06EX6DM2SJ",
                      "Checking your internet connectivity...")
        t1 = threading.Thread(target=check_internet_speed)
        t1.start()
        t1.join()
        app = "google"

        slack_message("U05FJ0V6QBZ", "D06EX6DM2SJ",
                      "Checking for relevant outages... ")

        time.sleep(3)
        slack_message("U05FJ0V6QBZ", "D06EX6DM2SJ",
                      "No outages detected")

        slack_log_case(
            "D06EX6DM2SJ", "Do you wish to log a case for you issue?")

    elif payload.lower().count("office") == 2:
        logger.info("Office option selected")
        app = "google"

        slack_message("U05FJ0V6QBZ", "D06EX6DM2SJ",
                      "Checking for relevant outages... ")

        time.sleep(3)
        slack_message("U05FJ0V6QBZ", "D06EX6DM2SJ",
                      "No outages detected")

    elif payload.lower().count("yes") == 2:
        slack_message("U05FJ0V6QBZ", "D06EX6DM2SJ",
                      "Logging supportforce case...")
        case_number = log_case()
        slack_message("U05FJ0V6QBZ", "D06EX6DM2SJ",
                      "Your case is created successfully - " + str(case_number))
    elif payload.lower().count("no") == 2:
        slack_message("U05FJ0V6QBZ", "D06EX6DM2SJ",
                      "Thank you")
