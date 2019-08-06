import sys
import os
import logging
import boto3    # AWS library   - external library.  See requirements.txt
import json

# Setup a logger object.  This will end up in CloudWatch
#
logger = logging.getLogger()
logger.setLevel(logging.INFO)

transcriptionFunction = os.environ.get("TRANSCRIPTION_FUNCTION")

client = boto3.client('lambda')

def handler(event, context):
    logger.info("Event: " + json.dumps(event))

    payload = {
        "streamARN": event["Details"]["ContactData"]["MediaStreams"]["Customer"]["Audio"]["StreamARN"],
        "startFragmentNum": event["Details"]["ContactData"]["MediaStreams"]["Customer"]["Audio"]["StartFragmentNumber"],
        "connectContactId": event["Details"]["ContactData"]["ContactId"],
        "transcriptionEnabled": True, #if event["Details"]["ContactData"]["Attributes"]["transcribeCall"] == "true" else False,
        "saveCallRecording": True, #if event["Details"]["ContactData"]["Attributes"]["saveCallRecording"] == "true" else False,
        "languageCode": event["Details"]["ContactData"]["Attributes"].get("languageCode", "en-US")
    }

    resp = client.invoke(
        FunctionName=transcriptionFunction,
        InvocationType='Event',
        Payload=json.dumps(payload)
    )
    logger.info("Invoke response: " + str(resp))

    result = "Success" if resp["StatusCode"] == 202 else "Failed"

    return {
        "lambdaResult": result
    }
