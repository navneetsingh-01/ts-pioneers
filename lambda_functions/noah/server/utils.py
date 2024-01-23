import requests
import speedtest
from .logger import logger
from .slack_interactions.api import slack_message


def getApplicationError(inputText):
    prompt = f"From the text provided after the semi colon, please infer the applcation the input has a problem with. After infering, return a json response as in this exact format without quotes- applicationReffered:appliation. The input is: {inputText}"
    url = "https://supportforce--spf24hack.sandbox.my.salesforce.com/services/data/v58.0/einstein/llm/prompt/generations"
    headers = {
        'Authorization': 'Bearer 00DO2000000nLP8!AQEAQNFQNO_Q6f4NLWf4T401dFMm1THl6iejczOnIGUI3lezlzcpZFhuDsugZmCZ.nezJ_cQztOf3F9diRFA.NiiWrSgWCs0',
        'Content-Type': 'application/json'
    }

    data = {
        "promptTextorId": prompt,
        "provider": "OpenAI",
        "additionalConfig": {"maxTokens": 512, "applicationName": "will-ai-m"}
    }
    response = requests.post(url, headers=headers, json=data)
    response = str(response.json()["generations"][0]["text"])
    return response


def check_internet_speed():
    st = speedtest.Speedtest()
    download = st.download()
    upload = st.upload()
    slack_message(None, "D06EX6DM2SJ", "Download: " +
                  str(download) + " | Upload: " + str(upload))
