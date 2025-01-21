from exceptions import GenerateTemplateFailed
from datetime import datetime
import json
import requests
from typing import TypedDict
from urllib.parse import urlencode


class MetaDataTransaction(TypedDict):
    account_id: str
    amount: str 
    motif: str
    created_at: str


class ClientDetails(TypedDict):
    ClientID: str
    FirstName: str 
    LastName: str
    Country: str
    Email: str
    Phone: str
    Spend: float
    Limit: float
    CardLimitReached: float
    ReloadingHistory: list


def _build_url(base_url: str, params: dict = None) -> str:
    """
    Builds the final URL with the given parameters.

    Args:
        base_url (str): The base URL.
        params (dict, optional): The URL parameters. Defaults to None.

    Returns:
        str: The final URL.
    """
    if params:
        return f"{base_url}?{urlencode(params)}"
    return base_url


def _cast_dynamodb_reload_history_to_reload_histories(dynamodb_reload_history):
    reload_history = []
    for dynamodb_reload in dynamodb_reload_history:
        reload = {
            'amount': float(dynamodb_reload['M']['amount']['N']),
            'payment_method': dynamodb_reload['M']['payment_method']['S'],
            'date': dynamodb_reload['M']['date']['S']
        }
        reload_history.append(reload)
    return reload_history


def _cast_item_dynamodb_to_client_details(client: dict) -> ClientDetails:
    """
    Converts a DynamoDB item (client) to a structured ClientDetails object.

    Args:
        client (dict): A dictionary representing the DynamoDB item with the following keys:
            - 'ClientID': The client's unique identifier (numeric).
            - 'FirstName': The client's first name (string).
            - 'LastName': The client's last name (string).
            - 'Country': The client's country (string).
            - 'Email': The client's email address (string).
            - 'Phone': The client's phone number (string).

    Returns:
        ClientDetails: A structured object containing client details.
    """


    return  {
        'ClientID': client['ClientID']['S'],
        'FirstName': client['FirstName']['S'],
        'LastName': client['LastName']['S'],
        'Country': client['Country']['S'],
        'Email': client['Email']['S'],
        'Phone': client['Phone']['S'],
        'Spend': float(client['Spend']['S']),
        'Limit': float(client['Limit']['S']),
        'CardLimitReached': float(client['CardLimitReached']['S']),
        'ReloadingHistory': json.loads(client['ReloadingHistory']['S']) if 'ReloadingHistory' in client else []
    }


def _cast_reload_history_to_dynamodb_reload_history(reload_history):
    dynamodb_reload_history = []
    for reload in reload_history:
        dynamodb_reload = {
            'M': {
                'amount': {'N': str(reload['amount'])},
                'payment_method': {'S': reload['payment_method']},
                'date': {'S': reload['date']}
            }
        }
        dynamodb_reload_history.append(dynamodb_reload)
    return dynamodb_reload_history


def _cast_client_details_to_item_dynamodb(client: ClientDetails) -> dict:
    """
    Converts client details to a DynamoDB item format.

    Args:
        client (ClientDetails): A dictionary containing client details.
            - 'ClientID': The unique client identifier.
            - 'FirstName': The first name of the client.
            - 'LastName': The last name of the client.
            - 'Country': The country of the client.
            - 'Email': The email address of the client.
            - 'Phone': The phone number of the client.
            - 'Spend': The spending amount of the client (float).
            - 'Limit': The spending limit for the client (float).

    Returns:
        dict: A dictionary representing the DynamoDB item.
    """


    return {
        'ClientID': {'S': str(client['ClientID'])},
        'FirstName': {'S': client['FirstName']},
        'LastName': {'S': client['LastName']},
        'Country': {'S': client['Country']},
        'Email': {'S': client['Email']},
        'Phone': {'S': client['Phone']},
        'Spend': {'S': str(client['Spend'])},
        'Limit': {'S': str(client['Limit'])},
        'CardLimitReached': {'S': str(client['CardLimitReached'])},
        'ReloadingHistory': {'S': json.dumps(client['ReloadingHistory'])},
    }




def _extract_meta_data_from_transaction_completed(transaction: dict) -> MetaDataTransaction:
    """
    Extracts the meta data from a completed transaction.

    Args:
        transaction (Dict): The completed transaction.

    Returns:
        MetaDataTransaction: The extracted meta data.
    """

    fee = 0
    if 'fee' in transaction['legs'][0]:
        fee = transaction['legs'][0]['fee']

    meta_data: MetaDataTransaction = {
        'created_at': datetime.fromisoformat(transaction['created_at'].replace("Z", "+00:00")).strftime("%d %B %Y"),
        'amount': abs(transaction['legs'][0]['amount']) + fee,
        'currency': transaction['legs'][0]['currency'],
        'motif': transaction['legs'][0]['description'],
    }

    return meta_data


def _generate_transactions_table(transactions: list[dict], table_title: str) -> str:
    """
    Generates a formatted string table from a list of transactions.

    Args:
        transactions (List[MetaDataTransactions]): The list of transactions.

    Returns:
        str: The formatted transactions table.
    """

    if not transactions:
        return "Aucune transaction à afficher."

    table_header = "| Date | Montant | Devise | Méthode paiement |"
    table_separator = "-" * len(table_header)
    rows = [table_title, table_header, table_separator]

    try:
        for transaction in transactions:
            row = f"| {transaction['Date']} | {transaction['Amount']} | EUR | {transaction['PaymentMethod']} |"
            rows.append(row)
    except Exception as e:
        raise GenerateTemplateFailed(str(e))
    
    table = "\n".join(rows)
    return table


def _convert_currency(amount: float, from_currency: str = "XAF", to_currency: str = "EUR") -> float:
    """
    Converts an amount from one currency to another using real-time exchange rates.

    Args:
        amount (float): The amount to convert.
        from_currency (str, optional): The source currency code (default is "XOF" for franc CFA d'Afrique centrale).
        to_currency (str, optional): The target currency code (default is "EUR" for euros).

    Returns:
        float: The converted amount in the target currency.

    Raises:
        ValueError: If the provided currencies are invalid or exchange rates cannot be fetched.
    """
    
    base_url = "https://api.exchangerate-api.com/v4/latest/"
    response = requests.get(base_url + from_currency)
    data = response.json()

    if 'rates' in data:
        rates = data['rates']
        if from_currency == to_currency:
            return amount
        if from_currency in rates and to_currency in rates:
            conversion_rate = rates[to_currency] / rates[from_currency]
            converted_amount = amount * conversion_rate
            return converted_amount
        else:
            raise ValueError("Invalid currency!")
    else:
        raise ValueError("Unable to fetch exchange rates!")
    
    
def _today() -> str:
    import datetime

    today = datetime.date.today()

    return f"{today.day}/{today.month}/{today.year}"
