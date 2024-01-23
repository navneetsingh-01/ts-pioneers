import os
import json
import sys
import logging
import hashlib
import time
import hmac
from typing import Dict, Any
from server.main import event_handler

logger = logging.getLogger('')
logger.setLevel(logging.INFO)
sh = logging.StreamHandler(sys.stdout)
formatter = logging.Formatter(
    '[%(asctime)s] %(levelname)s [%(filename)s.%(funcName)s:%(lineno)d] %(message)s', datefmt='%a, %d %b %Y %H:%M:%S')
sh.setFormatter(formatter)
logger.addHandler(sh)


def url_verification(event_body: Dict[Any, Any]):
    logger.info(event_body)
    if event_body.get("type") \
            and event_body["type"] == 'url_verification':
        return event_body["challenge"]
    else:
        return None


def get_signing_secret():
    return os.getenv("SIGNING_SECRET")


def validate_slack_request(headers: Dict[str, Any], request_body: str):
    # https://api.slack.com/authentication/verifying-requests-from-slack
    # get signing secret from AWS secret manager
    slack_signing_secret = get_signing_secret()
    # Step 1: Extract necessary information from the request
    timestamp = int(headers['X-Slack-Request-Timestamp'])
    logger.info("timestamp " + str(timestamp))

    logger.info(request_body)

    # Step 2: Verify the timestamp is recent
    if abs(time.time() - timestamp) > 60 * 5:
        logger.info(
            "timestamp failed validation for slack request verification")
        # The request timestamp is more than five minutes from local time.
        # It could be a replay attack, so let's ignore it.
        return False

    # Step 3: Construct the basestring
    sig_basestring = f'v0:{timestamp}:{request_body}'

    # Step 4: Compute the signature
    signature = 'v0=' + hmac.new(
        slack_signing_secret.encode('utf-8'),
        sig_basestring.encode('utf-8'),
        hashlib.sha256
    ).hexdigest()
    logger.info(f"Computed signature: {signature}")

    # Step 5: Compare the computed signature with the received signature
    slack_signature = headers['X-Slack-Signature']
    logger.info("headers['X-Slack-Signature'] = " + slack_signature)
    if hmac.compare_digest(signature, slack_signature):
        logger.info(
            "comparison between computed signature and slack signature succeeded")
        # The request came from Slack and is authentic
        return True

    logger.info(
        "comparison between computed signature and slack signature failed")
    return False


def lambda_handler(event: Dict[str, Any], context):
    logger.info(str(event))

    # validating that the slack request comes from slack
    if not validate_slack_request(event["headers"], event["body"]):
        raise Exception("Unable to verify that the message is from slack.")

    payload = json.loads(event["body"])
    slack_verification = url_verification(payload)
    if slack_verification:
        logger.info(slack_verification)
        # return "challenge" value from body if it's a "url_verification" request
        return {"statusCode": 200, "body": slack_verification}

    if event["headers"].get("X-Slack-Retry-Num"):
        return response

    try:
        logger.info("Payload: " + str(payload))
        event_handler(payload)
    except Exception as e:
        logger.info("Lambda handler error: " + str(e))

    response = {
        "statusCode": 200,
        "body": "Webhook received successfully"
    }
    return response
