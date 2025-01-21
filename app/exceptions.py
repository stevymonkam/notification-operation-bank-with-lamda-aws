class ClientNotFound(Exception):
    """
    Exception raised when a customer/client is not found in DynamoDB.

    Args:
        client_id (str): The ID of the client.
        message (str, optional): Custom error message (default is None).

    Attributes:
        client_id (str): The ID of the client causing the exception.
    """

    def __init__(self, client_id=None, message=None):
        if message is None:
            message = f"Customer {client_id} was not found in DynamoDB."
        super().__init__(message)
        self.client_id = client_id


class GenerateTemplateFailed(Exception):
    """
    Exception raised when generating a transaction list template fails.

    Args:
        message (str, optional): Custom error message (default is None).
    """

    def __init__(self, message=None):
        init_message = "Declined to generate transaction list template."
        if message is None:
            message = f"{init_message} {message}"
        else:
            message = init_message
        super().__init__(message)



class ActionDoesNotExist(Exception):
    """
    Custom exception class for actions that do not exist.

    Args:
        message (str, optional): A custom error message. Defaults to
            "The action you want to perform does not exist."

    Attributes:
        message (str): The error message associated with the exception.

    Example:
        try:
            raise ActionDoesNotExist("Invalid action")
        except ActionDoesNotExist as e:
            print(f"Error: {e}")
    """
    
    def __init__(self, message=None):
        if message is None:
            message = "The action you want to perform does not exist."
        super().__init__(message)


class TransactionAlreadyExecute(Exception):
    """
    Exception raised when a request with the same ID has already been executed.

    Args:
        transaction_id (str, optional): The ID of the request that was already executed.
        message (str, optional): Custom error message (default is generated based on request ID).

    Attributes:
        transaction_id (str): The ID of the transaction.

    Example:
        Usage example:
        >>> try:
        ...     # Some logic that checks if a transaction has already been executed
        ...     raise TransactionAlreadyExecute(transaction_id='12345')
        ... except TransactionAlreadyExecute as e:
        ...     print(f"Error: {str(e)}")
        Error: Transaction 12345 already executed.
    """
    
    def __init__(self, transaction_id=None, message=None):
        if message is None:
            message = f"Transaction {transaction_id} already executed."
        super().__init__(message)
        self.transaction_id = transaction_id
