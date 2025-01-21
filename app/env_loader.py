import json
import os
import boto3
from dotenv import load_dotenv

load_dotenv()

# Environment variables
ENV_DEV = os.getenv('ENV_DEV')  # Development environment flag
TAUX_EAZYCARD = os.getenv('TAUX_EAZYCARD')  # Taux eazycard
AWS_ACCESS_KEY = os.getenv('AWS_ACCESS_KEY')  # AWS access key
AWS_SECRET_KEY = os.getenv('AWS_SECRET_KEY')  # AWS secret key
AWS_REGION = os.getenv('AWS_REGION')  # AWS region
VERIFIED_EMAIL = os.getenv('VERIFIED_EMAIL')  # Verified email address
ADMIN_EMAILS = eval(os.getenv('ADMIN_EMAILS'))  # List of admin email addresses
COMMERCIAL_EMAILS = eval(os.getenv('COMMERCIAL_EMAILS'))  # List of commercial email addresses


# Secret configuration
SECRET_CLIENT_NAME = os.getenv('SECRET_CLIENT_NAME')  # Name of DynamoDB table client

# DynamoDB configuration
DYNAMODB_TABLE_CLIENT_NAME = os.getenv('DYNAMODB_TABLE_CLIENT_NAME')  # Name of DynamoDB table client

