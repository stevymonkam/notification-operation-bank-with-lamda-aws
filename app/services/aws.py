import json
from env_loader import AWS_ACCESS_KEY, AWS_REGION, AWS_SECRET_KEY, DYNAMODB_TABLE_CLIENT_NAME, ENV_DEV, SECRET_CLIENT_NAME, VERIFIED_EMAIL
import boto3


def init_secret_manager_client():
    """
    Creates and returns a DynamoDB client using the specified credentials and region.
    
    Returns:
        boto3.client: The initialized DynamoDB client.
    """


    return boto3.client(
        'secretsmanager', 
        aws_access_key_id=AWS_ACCESS_KEY,
        aws_secret_access_key=AWS_SECRET_KEY,
        region_name=AWS_REGION
    ) if ENV_DEV else boto3.client('secretsmanager')


def init_ses_client():
    """
    Creates and returns a DynamoDB client using the specified credentials and region.
    
    Returns:
        boto3.client: The initialized DynamoDB client.
    """


    return boto3.client(
        'ses', 
        aws_access_key_id=AWS_ACCESS_KEY,
        aws_secret_access_key=AWS_SECRET_KEY,
        region_name=AWS_REGION
    ) if ENV_DEV else boto3.client('ses')


def init_dynamodb_client():
    """
    Creates and returns a DynamoDB client using the specified credentials and region.
    
    Returns:
        boto3.client: The initialized DynamoDB client.
    """


    return boto3.client(
        'dynamodb', 
        aws_access_key_id=AWS_ACCESS_KEY,
        aws_secret_access_key=AWS_SECRET_KEY,
        region_name=AWS_REGION
    ) if ENV_DEV else boto3.client('dynamodb')


def retrieve_secret(secret_id=SECRET_CLIENT_NAME) -> dict:
    secrets_manager_client = init_secret_manager_client()

    get_secret_value_response = secrets_manager_client.get_secret_value(
        SecretId=secret_id
    )

    return json.loads(get_secret_value_response['SecretString'])


def send_email(to_addresses: list[str], bcc_addresses: list[str], body_message: str, subject_message: str, Source=VERIFIED_EMAIL) -> str:
    """_summary_

    Args:
        to_addresses (list[str]): List emails to addresses
        bcc_addresses (list[str]): List emails to cache
        body_message (str): Mail message
        subject_message (str): Mail Subject

    Returns:
        str: Success message
    """    

    ses = init_ses_client()
    ses.send_email(
        Source=Source,
        Destination={
            'ToAddresses': to_addresses,
            'BccAddresses': bcc_addresses
        },
        Message={
            'Subject': {'Data': subject_message},
            'Body': {'Text': {'Data': body_message }}
        }
    )

    return 'Success!'


def create_item(item: dict, table_name=DYNAMODB_TABLE_CLIENT_NAME) -> dict:
    
    dynamodb_client = init_dynamodb_client()
    dynamodb_client.put_item(TableName=table_name, Item=item)
    return item


def retrieve_item(item_id: str, table_name=DYNAMODB_TABLE_CLIENT_NAME) -> dict:
    """
    Retrieves a client from the DynamoDB database.

    Args:
        item_id (str): The unique identifier of the client.

    Returns:
         ClientDetails: The client details
    """
    
    dynamodb_client = init_dynamodb_client()

    return dynamodb_client.get_item(
        TableName=table_name,
        Key={
            'ClientID': {'S': str(item_id)}
        }
    ) 


def retrieve_all_items(table_name=DYNAMODB_TABLE_CLIENT_NAME) -> dict:
    dynamodb_client = init_dynamodb_client()

    return dynamodb_client.scan(TableName=table_name)


def update_item(item_id: str, update_expression: str, attribute_names: dict, attribute_values: dict, table_name=DYNAMODB_TABLE_CLIENT_NAME) -> dict:
    """
    Updates a client's attributes in DynamoDB.

    Args:
        item_id (str): The unique client identifier.
        update_expression (str): The update expression for modifying attributes.
        attribute_names (dict): A dictionary of attribute names and their placeholders.
        attribute_values (dict): A dictionary of attribute values and their placeholders.

    Returns:
        dict: The response from DynamoDB after updating the item.
    """

    dynamodb_client = init_dynamodb_client()

    return dynamodb_client.update_item(
        TableName=table_name,
        Key={
            'ClientID': {'S': str(item_id)}
        },
        UpdateExpression=update_expression,
        ExpressionAttributeNames=attribute_names,
        ExpressionAttributeValues=attribute_values
    )


def delete_item(item_id: str, table_name=DYNAMODB_TABLE_CLIENT_NAME) -> dict:
    """
    Deletes a item from the DynamoDB table.

    Args:
        item_id (str): The ID of the item to be deleted.

    Returns:
        dict: The response of the delete operation.
    """
    dynamodb_client = init_dynamodb_client()

    return dynamodb_client.delete_item(
        TableName=table_name,
        Key={
            'ClientID': {'S': str(item_id)}
        }
    )
