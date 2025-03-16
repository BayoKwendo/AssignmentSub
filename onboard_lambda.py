import json
import boto3
import uuid
import logging

# Initialize DynamoDB client
dynamodb = boto3.client('dynamodb')
table_name = 'ClientData'  # DynamoDB table name from environment variable or hardcoded

# Set up logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    # Parse incoming event
    try:
        body = json.loads(event['body'])
        client_name = body['clientName']
        client_phone = body['clientPhone']
        
        # Generate a unique client ID
        client_id = str(uuid.uuid4())
        
        # Create a new client record for DynamoDB
        item = {
            'clientID': {'S': client_id},
            'clientName': {'S': client_name},
            'clientPhone': {'S': client_phone},
            'createdAt': {'S': str(uuid.uuid1())},  # Use timestamp-based UUID for createdAt
        }

        # Put the item into DynamoDB
        response = dynamodb.put_item(
            TableName=table_name,
            Item=item
        )
        
        logger.info(f"Successfully onboarded client: {client_id}")

        return {
            'statusCode': 200,
            'body': json.dumps({
                'status': 'success',
                'clientID': client_id
            })
        }

    except Exception as e:
        logger.error(f"Error onboarding client: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps({
                'status': 'error',
                'message': 'Failed to onboard client',
                'error': str(e)
            })
        }
