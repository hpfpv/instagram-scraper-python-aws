import json
import os
import boto3
import logging

client = boto3.client('dynamodb', region_name='us-east-1')
logger = logging.getLogger()
logger.setLevel(logging.INFO)


def lambda_handler(event, context):
    logger.info(event)

    log = {}
    log["function"] = "record_events"

    account_to_mention = event['pathParameters']['account_to_mention']
    requestId = event['requestContext']['requestId']
    
    record = {
        "requestId" : { "S": requestId },
        "account" : { "S": account_to_mention },
    }

    log["message"] = json.dumps(record)

    logger.info(json.dumps(log))

    response = client.put_item(
        TableName=os.environ['EVENTS_TABLE'],
        Item=record,
        )  
    responseBody = {
        'requestId' : requestId
    }
    return {
        'statusCode': 202,
        'headers': {
            'Access-Control-Allow-Origin': 'https://instastories.houessou.com',
            'Access-Control-Allow-Headers': 'Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token',
            'Access-Control-Allow-Methods': 'GET, POST',
            'Content-Type': 'application/json'
        },
        'body': json.dumps(responseBody)  
    }