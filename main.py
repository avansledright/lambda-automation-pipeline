import boto3
from botocore.exceptions import ClientError
import sys
import base64
import json
import os 

def send_sns(message):
    client = boto3.client("sns", region_name="us-west-2")
    try:
        client.publish(
            TopicArn=os.environ['sns_topic_arn'],
            Message=message,
            Subject='Automated Lambda Testing Results'
        )
        return True
    except ClientError as e:
        print("Failed to send message to SNS")
        print(e)


def lambda_invoke(payload, function_name):
    client = boto3.client('lambda', region_name="us-west-2")
    try:
        response = client.invoke(
            FunctionName=function_name,
            InvocationType='RequestResponse',
            LogType='Tail',
            Payload=json.dumps(payload)
        )
        return response
    except ClientError as e:
        print("Failed to invoke Lambda")
        print(e)
        return False

if __name__ == "__main__":
    print("Starting lambda testing")
    lambda_info = json.loads(sys.argv[1])
    print(lambda_info)
    results = {}
    for _lambda in lambda_info:
        print(_lambda)
        for lambda_name, test_event in _lambda.items():
            response = lambda_invoke(test_event, lambda_name)
            if  response != False:
                response_payload = json.loads(response['Payload'].read())
                results.update(
                    {
                        lambda_name: {
                            'Response': response_payload,
                            'StatusCode': response['StatusCode']
                        }
                    }
                )
    print("Sending results to SNS")
    if send_sns(results) == True:
        print("Successfully sent message")
    else:
        print("Failed to send results")  
    print(results)  