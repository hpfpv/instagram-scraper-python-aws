import boto3
import json
import os
import logging

client = boto3.client('dynamodb', region_name='us-east-1')
logger = logging.getLogger()
logger.setLevel(logging.INFO)

def getDocumentJson(item):
    logger.info(item)
    doc = {}
    doc["requestId"] = item["requestId"]["S"]
    doc["time"] = item["time"]["S"]
    doc["account"] = item["account"]["S"]
    doc["stories"] = item["stories"]["S"]
    return doc

def retrieveStories(requestId):
    response = client.get_item(
        TableName=os.environ['EVENTS_TABLE'],
        Key={
            'requestId': {
                'S': requestId
            }
        }
    )
    response = getDocumentJson(response["Item"])
    return json.dumps(response)

def lambda_handler(event, context):
    logger.info(event)

    log = {}
    log["function"] = "retrieve_stories"

    requestId = event['pathParameters']['requestId']
    loop = True
    while loop:
        items = retrieveStories(requestId)
        log["message"] = json.dumps(items)
        if items["stories"] :
            logger.info(json.dumps(log))
            loop = False
            return {
                'statusCode': 200,
                'headers': {
                    'Access-Control-Allow-Origin': 'https://todo.houessou.com',
                    'Access-Control-Allow-Headers': 'Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token',
                    'Access-Control-Allow-Methods': 'GET',
                    'Content-Type': 'application/json'
                },
                'body': items
            }