import json
import os
import boto3
from botocore.exceptions import ClientError

# Initialize DynamoDB client
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(os.environ['TABLE_NAME'])

# Initialize Cognito client (optional)
cognito = boto3.client('cognito-idp')
user_pool_id = os.getenv('USER_POOL_ID')

def lambda_handler(event, context):
    try:
        # Parse input data
        client_data = json.loads(event['body'])
        tenant_id = client_data['tenantName']
        client_id = client_data['clientName']
        
        # Create new client record in DynamoDB
        response = table.put_item(
            Item={
                'TenantID': tenant_id,
                'ClientID': client_id,
                'ClientPhone': client_data['clientPhone'],
                'ClientEmail': client_data['clientEmail']
            }
        )

        # Optionally create a Cognito user (if needed)
        if user_pool_id:
            create_cognito_user(client_data)

        return {
            'statusCode': 200,
            'body': json.dumps({'message': 'Client onboarded successfully', 'data': client_data})
        }

    except ClientError as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'message': 'Error processing onboarding', 'error': str(e)})
        }

def create_cognito_user(client_data):
    try:
        cognito.admin_create_user(
            UserPoolId=user_pool_id,
            Username=client_data['clientEmail'],
            UserAttributes=[
                {'Name': 'email', 'Value': client_data['clientEmail']},
                {'Name': 'phone_number', 'Value': client_data['clientPhone']}
            ]
        )
    except ClientError as e:
        print(f"Error creating Cognito user: {e}")
