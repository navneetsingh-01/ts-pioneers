import os
import requests
import threading
import time
from .logger import logger
from .slack_interactions.api import slack_message, conversation_history, slack_location_message, slack_log_case, conversation_history_ai, slack_reset_ad, slack_ad_link_btn, slack_forget_password
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

    if 'gmeet' in str(application).lower() or 'google' in str(application).lower():
        slack_message(
            user, channel_id, "Thanks! I understand you’re having issues with Google Meet. Let me see what I can do to help! ")
        slack_location_message(channel_id, "Please choose your location")
    elif 'AD' in str(application).lower() or 'ad' in str(application).lower():
        # slack_message(
        #     user, channel_id, "Okay, I got it. Here’s a link where you can reset your password\nhttps://sfdcpwd.internal.salesforce.com/RDWeb/Pages/en-US/password.aspx")
        slack_forget_password(channel_id, "do you remember you current")
    elif 'thank' in str(application).lower() or 'no' in str(application).lower():
        slack_message(
            user, channel_id, "Awesome! I’m so glad to hear it! Have a good one!")
    elif 'hi' in str(application).lower() or 'hello' in str(application).lower() or 'who' in str(application).lower():
        slack_message(user, channel_id, "Hi! :wave: I’m NOAH. I can help you with network or app issues you might be experiencing by fetching all sorts of helpful tools and resources you can use, as well as dig for incidents that might relate to what you’re experiencing. What’s going on?")
    else:
        slack_message(user, channel_id,
                      "I can't handle this request. Look out for future updates :)")

    # conversation_history(os.getenv("INCIDENTS_CHANNEL"))
    # log_case()


def handle_interactive_response(payload):
    if payload.lower().count("raise"):
        slack_message("U05FJ0V6QBZ", "D06EX6DM2SJ",
                      "Hi there :wave: I’m NOAH. How can I help you?")
    elif payload.lower().count("home") == 2:
        logger.info("Home option selected")
        slack_message("U05FJ0V6QBZ", "D06EX6DM2SJ",
                      "Okay! Now I’m going to quickly check your internet connectivity and let you know how that’s doing.")
        t1 = threading.Thread(target=check_internet_speed)
        t1.start()
        t1.join()

        slack_message("U05FJ0V6QBZ", "D06EX6DM2SJ",
                      "Let’s keep that in mind but also look for any active incidents relating to this issue.")

        time.sleep(3)

        slack_message("U05FJ0V6QBZ", "D06EX6DM2SJ",
                      "Ah, I found one! Here’s the most recent update on it (I found this in the #broadcast-bt-incidents Slack channel :slightly_smiling_face:)\n\n")

        slack_message("U05FJ0V6QBZ", "D06EX6DM2SJ",
                      " :link: https://internal-sbx.slack.com/archives/C06FPEGPRUY/p1706068688725979|Outage \n\n_We currently have 14 other users checking for outages for Google Meet_")

        slack_message(
            "U05FJ0V6QBZ", "D06EX6DM2SJ", "Since there’s an active incident, you might want to keep an eye on that Slack channel for updates, but we shouldn’t need to log a ticket for you. Is there anything else I can help you with?")

    elif payload.lower().count("office") == 2:
        logger.info("Office option selected")

        slack_message("U05FJ0V6QBZ", "D06EX6DM2SJ",
                      "Looking for any active incidents relating to this issue")

        # incidents = conversation_history_ai("D06EX6DM2SJ", application)

        time.sleep(3)
        slack_message("U05FJ0V6QBZ", "D06EX6DM2SJ",
                      "Ah, I found one! Here’s the most recent update on it (I found this in the #broadcast-bt-incidents Slack channel :slightly_smiling_face:)\n\n")

        slack_message("U05FJ0V6QBZ", "D06EX6DM2SJ",
                      " :link: https://internal-sbx.slack.com/archives/C06FPEGPRUY/p1706068688725979|Outage \n\nWe currently have 3 other users checking for outages for Google Meet")
        slack_message(
            "U05FJ0V6QBZ", "D06EX6DM2SJ", "Since there’s an active incident, you might want to keep an eye on that Slack channel for updates, but we shouldn’t need to log a ticket for you. Is there anything else I can help you with?")

    elif payload.lower().count("yes") == 2:
        if payload.count("FORGETPASSWORD"):
            slack_ad_link_btn("D06EX6DM2SJ", "TEST")
            time.sleep(5)
            slack_reset_ad("D06EX6DM2SJ", "Is your AD Password reset?")
        elif payload.count("ADPASSWORD"):
            slack_message("U05FJ0V6QBZ", "D06EX6DM2SJ",
                          "Great!!")

    elif payload.lower().count("no") == 2:
        if payload.count("FORGETPASSWORD"):
            slack_message("U05FJ0V6QBZ", "D06EX6DM2SJ",
                          "Refer to the below link to reset your password\nhttps://concierge.it.salesforce.com/articles/en_US/Supportforce_Article/Techforce-Password-Guidance-and-Support")
            time.sleep(2)
            slack_message("U05FJ0V6QBZ", "D06EX6DM2SJ",
                          "Is there anything else I can help you with?")
        elif payload.count("ADPASSWORD"):
            slack_message("U05FJ0V6QBZ", "D06EX6DM2SJ",
                          "No worries!! I'll create a case for you.")
            time.sleep(10)
            # case = log_case()
            case_number = "15758126"
            slack_message("U05FJ0V6QBZ", "D06EX6DM2SJ",
                          "All set! I got a case created for you. Here’s the Case #:" + str(case_number) + "\nYou can check progress using the Ask Concierge app.")
            time.sleep(2)
            slack_message("U05FJ0V6QBZ", "D06EX6DM2SJ",
                          "Is there anything else I can help you with?")
        else:
            slack_message("U05FJ0V6QBZ", "D06EX6DM2SJ",
                          "Awesome! I’m so glad to hear it! Have a good one!")
