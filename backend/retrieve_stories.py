import boto3
import json
import os
import logging
import time

client = boto3.client('dynamodb', region_name='us-east-1')
logger = logging.getLogger()
logger.setLevel(logging.INFO)

def getDocumentJson(item):
    doc = {}
    doc["requestId"] = item["requestId"]["S"]
    doc["time"] = item["time"]["S"]
    doc["account"] = item["account"]["S"]
    doc["completed"] = item["completed"]["BOOL"]
    if item["completed"]["BOOL"] == True:
        doc["stories"] = item["stories"]["S"]
    return doc

def retrieveStories(requestId):
    # loop = True
    # while loop:
    response = client.get_item(
        TableName=os.environ['EVENTS_TABLE'],
        Key={
            'requestId': {
                'S': requestId
            }
        }
    )
    # if response['Item']['completed']['BOOL'] == True:
    #     loop = False
    # else:
    #     time.sleep(10)
    response = getDocumentJson(response["Item"])
    return json.dumps(response)

def lambda_handler(event, context):
    logger.info(event)

    log = {}
    log["function"] = "retrieve_stories"

    requestId = event['pathParameters']['requestId']
    items = retrieveStories(requestId)
    logger.info(items)
        
    return {
        'statusCode': 200,
        'headers': {
            'Access-Control-Allow-Origin': 'https://instastories.houessou.com',
            'Access-Control-Allow-Headers': 'Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token',
            'Access-Control-Allow-Methods': 'GET',
            'Content-Type': 'application/json'
        },
        'body': items
    }