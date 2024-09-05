import json
from datetime import datetime

import boto3

from settings import ENVIRONMENT


def log_to_cloudwatch(query):
    if ENVIRONMENT != "test":
        client = boto3.client("logs")

        client.put_log_events(
            logGroupName='autocomplete',
            logStreamName='analytics-logs',
            logEvents=[
                {
                    'timestamp': int(datetime.now().timestamp()*1000),
                    'message': json.dumps({
                        "query": query.strip().lower()
                    })
                },
            ]
        )
