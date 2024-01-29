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
    download = str(st.download())
    upload = str(st.upload())
    download = download[0:2] + "." + download[2:5]
    upload = upload[0:2] + "." + upload[2:5]
    slack_message(None, "D06EX6DM2SJ", "Here is what I found: \n :dart: Download Speed: " +
                  str(download) + " Mbps\n :dart: Upload Speed: " + str(upload) + "Mbps")
    msg = "great performance"
    download = float(download)
    if download >= 20 and download < 50:
        msg = "good performance"
    elif download >= 5 and download < 20:
        msg = "low performance"
    elif download >= 0 and download < 5:
        msg = "poor performace"
    slack_message(None, "D06EX6DM2SJ",
                  "This means your internet performance is currently considered having a " + msg)
