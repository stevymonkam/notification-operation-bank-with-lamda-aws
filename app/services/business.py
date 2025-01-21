import json
from datetime import datetime
from env_loader import (
    ADMIN_EMAILS,
)
from exceptions import ClientNotFound
from factories import (
    ClientDetails,
    _cast_client_details_to_item_dynamodb, 
    _cast_item_dynamodb_to_client_details,
    _convert_currency,
    _generate_transactions_table,
    _today
)
from services.aws import create_item, retrieve_all_items, retrieve_item, send_email, update_item


def retrieve_a_client(client_id: str) -> ClientDetails:
    """
    Retrieves a client from the DynamoDB database.

    Args:
        client_id (str): The unique identifier of the client.

    Returns:
         ClientDetails: The client details
    """

    response = retrieve_item(client_id)
 
    # Return the items from the response
    item = response.get('Item')
    if item is None:
        raise ClientNotFound(client_id)

    client: ClientDetails = _cast_item_dynamodb_to_client_details(item)
    return client


def retrieve_all_clients() -> list[ClientDetails]:
    """
    Retrieves all customers from the DynamoDB table.

    Returns:
        list[ClientDetails]: A list of client details.
    """

    response = retrieve_all_items()

    return list(map(lambda item: _cast_item_dynamodb_to_client_details(item), response['Items']))


def retrieve_a_reload(client_id: str) -> str: 
    """
    Sends transaction history to customers via email.

    Retrieves completed transactions for each customer, generates a transaction table,
    and sends an email containing the transaction history.

    Args:
        None

    Returns:
        str: Success message
    """

    client = retrieve_a_client(client_id)
    for objet in client['ReloadingHistory']:
        objet["Name"] = f"{client['FirstName']} {client['LastName']}"
    return {
        'statusCode': 200,
        'body': json.dumps(sorted(client['ReloadingHistory'], key=lambda x: datetime.strptime(x['Date'], '%d/%m/%Y'), reverse=True)),
    }


def retrieve_all_reload() -> str: 
    """
    Sends transaction history to customers via email.

    Retrieves completed transactions for each customer, generates a transaction table,
    and sends an email containing the transaction history.

    Args:
        None

    Returns:
        str: Success message
    """

    clients = retrieve_all_clients()
    reload_histories = []
    for client in clients:
        for objet in client['ReloadingHistory']:
            objet["Name"] = f"{client['FirstName']} {client['LastName']}"
        reload_histories = [*reload_histories, *client['ReloadingHistory']]

    return {
        'statusCode': 200,
        'body': json.dumps(sorted(reload_histories, key=lambda x: datetime.strptime(x['Date'], '%d/%m/%Y'), reverse=True)),
    }


def create_client(client: ClientDetails) -> str:
    """
    Creates a client record in DynamoDB.

    Args:
        client (ClientDetails): A dictionary containing client details.

            'ClientID': The unique client identifier.
            'FirstName': The first name of the client.
            'LastName': The last name of the client.
            'Country': The country of the client.
            'Email': The email address of the client.
            'Phone': The phone number of the client.
            'Spend': The spending amount of the client.
            'Limit': The spending limit for the client.
            'CardLimitReached': Consecutive number of failed customer transactions due to card limit reached.

    Returns:
        str: A message indicating successful client registration.
    """


    try:
        client = retrieve_a_client(client['ClientID'])
        return {
            'statusCode': 400,
            'body': json.dumps({'message': 'Client already exists.'})
        }
    
    except ClientNotFound:
        taux_eazycard = float(client['Rate'])
        if taux_eazycard < 0 or taux_eazycard > 1:
            return {
                'statusCode': 400,
                'body': json.dumps({'message': 'The rate is incorrect it must be between 0 and 1.'})
            }
        if client['Limit'] < 0: 
            return {
                'statusCode': 400,
                'body': json.dumps({'message': 'Refill amount cannot be negative'})
            }
        limit_EUR = round(_convert_currency(float(client['Limit'])), 2)
        client['Limit'] = round(limit_EUR - taux_eazycard * limit_EUR, 2)
        client['Spend'] = 0
        client['CardLimitReached'] = 0
        client['ReloadingHistory'] = [{
            "Amount": client['Limit'],
            "PaymentMethod": client['PaymentMethod'],
            "Date": _today(),
            "clientID": client['ClientID'],
        }]
        

        item = _cast_client_details_to_item_dynamodb(client)
        
        create_item(item)

        message = f"""Bonjour {client['FirstName']} {client['LastName']}
Nous avons le plaisir de vous informer que votre compte EAZYCard a été créé avec succès.
Détails du compte :
    - ID du compte : {client['ClientID']}
    - Date de création : {_today()}
    - Recharge initiale : {limit_EUR}
    - Solde actuel : {client['Limit']} EUR

Pour toute communication future, veuillez s'il vous plaît préciser l'ID de votre compte : {client['ClientID']}

Nous restons à votre disposition pour toute question ou assistance complémentaire.
Cordialement,
L'équipe EAZYCard
"""

        # send_email(ADMIN_EMAILS, message, 'CONFIRMATION DE CRÉATION DE VOTRE COMPTE EAZYCARD')
        send_email([client['Email']], ADMIN_EMAILS, message, 'CONFIRMATION DE CRÉATION DE VOTRE COMPTE EAZYCARD')

        print("Success: Client created successfully.")
        return {
            'statusCode': 201,
            'body': json.dumps({
                'message': 'Client created successfully.',
                'conversion_amount': limit_EUR,
                'new_limit': client['Limit']
            })
        }


def card_recharge(client_id: str, amount: float, rate: float, currency: str, payment_method: str) -> str:
    """
    Recharges a client's card by updating the spending limit.

    Args:
        client_id (str): The unique client identifier.
        amount (float): The recharge amount in the client's currency.

    Returns:
        str: A message indicating successful card recharge.
    """
    try:
        client = retrieve_a_client(client_id)
    except ClientNotFound as e:
        message = f'{str(e)}'
        return {
            'statusCode': 404,
            'body': json.dumps({'message': f'Client {client_id} not found.'})
        }
    
    amount_eur = round(_convert_currency(amount, currency), 2)
    taux_eazycard = float(rate)
    if taux_eazycard < 0 or taux_eazycard > 1:
        return {
            'statusCode': 400,
            'body': json.dumps({'message': 'The rate is incorrect it must be between 0 and 1.'})
        }
    if amount_eur < 0: 
        return {
            'statusCode': 400,
            'body': json.dumps({'message': 'Refill amount cannot be negative'})
        }
    new_amount_eur = amount_eur - taux_eazycard * amount_eur
    new_limit = round(float(client['Limit']) + new_amount_eur, 2)
    balance = round(new_limit - float(client['Spend']), 2)
    recharge = {
        "Amount": amount_eur,
        "PaymentMethod": payment_method,
        "Date": _today(),
        "clientID": client['ClientID']
    }
    update_expression = 'SET #field1 = :field1, #field2 = :field2, #field3 = :field3'
    attribute_names = {
        '#field1': 'Limit',
        '#field2': 'CardLimitReached',
        '#field3': 'ReloadingHistory'
    }
    attribute_values = {
        ':field1': {'S': str(new_limit)},
        ':field2': {'S': str(0)},
        ':field3': {'S': json.dumps([recharge, *client['ReloadingHistory']])},
    }

    update_item(client_id, update_expression, attribute_names, attribute_values)

    if payment_method == 'Remboursement':
        message = f"""Bonjour {client['FirstName']} {client['LastName']},
Nous avons le plaisir de vous informer que votre remboursement EAZYCard a été réalisée avec succès.
Détails de la transaction :
    - Montant du remboursement : {amount_eur} EUR
    - Date du remboursement : {_today()}
    - Nouveau solde : {balance} EUR

Nous vous remercions pour votre confiance. 

Nous restons à votre disposition pour toute question ou assistance complémentaire.
Cordialement,
L'équipe EAZYCard
"""
        # send_email(ADMIN_EMAILS, message, 'VOTRE REMBOURSEMENT EAZYCard A REUSSI')
        send_email([client['Email']], ADMIN_EMAILS, message, 'VOTRE REMBOURSEMENT EAZYCard A REUSSI')

    else:
        message = f"""Bonjour {client['FirstName']} {client['LastName']},
Nous avons le plaisir de vous informer que votre recharge EAZYCard a été réalisée avec succès.
Détails de la transaction :
    - Montant de la recharge : {amount_eur} EUR
    - Date de la recharge : {_today()} 
    - Nouveau solde : {balance} EUR

Nous vous remercions de votre confiance. 

Nous restons à votre disposition pour toute question ou assistance complémentaire.
Cordialement,
L'équipe EAZYCard
"""

        # send_email(ADMIN_EMAILS, message, 'VOTRE RECHARGE EAZYCard A REUSSI')
        send_email([client['Email']], ADMIN_EMAILS, message, 'VOTRE RECHARGE EAZYCard A REUSSI')

    return {
        'statusCode': 200,
        'body': json.dumps({
            'message': f'Client {client_id} recharge successful.',
            'conversion_amount': amount_eur,
            'new_limit': new_limit
        })
    }


def send_transaction_history_to_customers() -> str: 
    """
    Sends transaction history to customers via email.

    Retrieves completed transactions for each customer, generates a transaction table,
    and sends an email containing the transaction history.

    Args:
        None

    Returns:
        str: Success message
    """

    clients = retrieve_all_clients()
    for client in clients:
        transactions = client['ReloadingHistory']
        table_title = 'Voici votre historique des recharges\n'
        balance = round(float(client['Limit']) - float(client['Spend']), 2)
        message = f"{client['FirstName']} {client['LastName']}\nVotre solde actuel est {balance} EUR\n{_generate_transactions_table(transactions, table_title)}"
        send_email([client['Email']], ADMIN_EMAILS, message, 'VOTRE HISTORIQUE DE TRANSACTION EAZYCard ENVOYE CHAQUE SEMAINE')

    return {
        'statusCode': 200,
        'body': json.dumps('Email history transaction sent successfully'),
    }

