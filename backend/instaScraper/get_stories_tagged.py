
from instaScraper.modules.stories import get_followers_stories, check_for_new_stories, story_time_str
from instaScraper.modules.download import profile_picture, story_media
from instaloader import exceptions as Exceptions

import os
import requests
import boto3
import json
from datetime import datetime
import logging
import sys

client = boto3.client('dynamodb', region_name='us-east-1')
logger = logging.getLogger()
logger.setLevel(logging.INFO)


def lambda_handler(event, context):
    logger.info(event)
    for record in event ['Records']:
        if record['eventName'] == 'INSERT':
            requestId = record['dynamodb']['NewImage']['requestId']['S']
            account_to_mention = record['dynamodb']['NewImage']['account']['S']

            try:
                storiesJson = check_for_new_stories(requestId, account_to_mention)
            except Exception as e:
                logger.info(e)
                response = client.update_item(
                    TableName=os.environ['EVENTS_TABLE'],
                    Key={
                        'requestId': {
                            'S': requestId,
                        }
                    },
                    UpdateExpression="SET request_state = :s",
                    ExpressionAttributeValues={
                        ':s': {'S': "error"}
                    }
                )
                response = {}
                response["Update"] = "Success"
            else:
                response = client.update_item(
                    TableName=os.environ['EVENTS_TABLE'],
                    Key={
                        'requestId': {
                            'S': requestId,
                        }
                    },
                    UpdateExpression="SET stories = :s, request_state = :c",
                    ExpressionAttributeValues={
                        ':s': {'S': json.dumps(storiesJson)},
                        ':c': {'S': "completed"}
                    }
                )
                response = {}
                response["Update"] = "Success"
                return response
            

