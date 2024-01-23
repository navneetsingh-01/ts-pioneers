import os
import requests
from .actions import create, describe
from ..logger import logger

SF_ACCESS_TOKEN = os.getenv("SF_ACCESS_TOKEN")
SF_INSTANCE_URL = os.getenv("SF_INSTANCE_URL")

headers = {
    "Content-type": "application/json",
    "Authorization": "Bearer " + SF_ACCESS_TOKEN
}


def get_record_type_id(record_type):
    response = requests.get(
        SF_INSTANCE_URL + describe("Case"), headers=headers)
    recordTypes = response.json()["recordTypeInfos"]
    for i in range(0, len(recordTypes)):
        if recordTypes[i]["name"] == record_type:
            return recordTypes[i]["recordTypeId"]
    return ""


def log_case():

    contact_id = "003O2000007Nu3tIAC"
    subject = "Subject goes here..."
    case_desc = "Description goes here..."
    record_type_id = get_record_type_id("Ticket Record Type")

    case_details = {
        "RecordTypeId": record_type_id,
        "ContactId": contact_id,
        "Status": "New",
        "Origin": "InfraOps Network",
        "Priority": "Standard",
        "Description": case_desc,
        "Internal_Support_Category__c": "IT - InfraOps - Network",
        "Subject": subject
    }

    try:
        response = requests.post(
            SF_INSTANCE_URL + create("Case"),  headers=headers, json=case_details)
        logger.info(str(response.json()))
    except Exception as e:
        logger.info("Something went wrong: " + str(e))
