import json
from functools import wraps
from exceptions import (
    ActionDoesNotExist,
    ClientNotFound
)

from services.aws import retrieve_secret
from services.business import card_recharge, create_client, retrieve_a_reload, retrieve_all_reload, send_transaction_history_to_customers
    
def auth(func):
    @wraps(func)
    def wrapper(event, context):
        print('CONTEXT:')
        print(context)

        print('EVENT:')
        print(event)
        body = json.loads(event['body'])
        if 'action' in body: 
            api_key = event.get('headers', {}).get('x-api-key')
            secrets = retrieve_secret()
            if api_key and api_key == secrets['EAZYCARD_API_KEY']:
                return func(event, context)
            else:
                return {
                    'statusCode': 401,
                    'body': json.dumps({'error': 'Invalid API key'})
                }
        return func(event, context)
    return wrapper

    
def lambda_handler(event, context):

    try: 
        body = json.loads(event['body'])
    except KeyError:
        if event['action'] == 'HISTORY_TRANSACTION':
            return send_transaction_history_to_customers()
    return compute(event, context)


@auth
def compute(event, context):
    body = json.loads(event['body'])
    # body = event
    try:
        action = body['action']
        if action == 'CREATE_CLIENT':
            return create_client(body['data'])
        elif action == 'CARD_RECHARGE':
            return card_recharge(body['data']['ClientID'], body['data']['Limit'], body['data']['Rate'], body['data']['Currency'] if body['data']['Currency'] else 'XAF', body['data']['PaymentMethod'])
        elif action == 'HISTORY_RELOAD':
            if 'data' in body and 'ClientID' in body['data']:
                return retrieve_a_reload(body['data']['ClientID'])
            return retrieve_all_reload()
        try:
            raise ActionDoesNotExist
        except ActionDoesNotExist as e:
            print(f"Error: {e}")
            return {
                "statusCode": 400, 
                "body": json.dumps(f"Error: {e}")
            }
    except ClientNotFound as e:
        message = f'{str(e)}\n{body}'
        print(f"Info: {str(e)}")  
        # notification_of_non_existence_constumer_by_email(message)   
        return {
            "statusCode": 200, 
            "body": json.dumps(f"Info: {e}")
        } 