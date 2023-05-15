# api.py
import google.auth
from google.auth.transport.requests import Request
from google.oauth2 import id_token
from google.auth.transport import requests
from googleapiclient.discovery import build

def get_phone_number(access_token):
    try:
        # Set up credentials
        creds, project = google.auth.default()
        creds.refresh(Request())
        id_info = id_token.verify_oauth2_token(access_token, requests.Request(), creds.client_id)

        # Initialize the People API service
        service = build('people', 'v1', credentials=creds)

        # Get the user's phone numbers
        response = service.people().get(resourceName='people/me', personFields='phoneNumbers').execute()
        phone_numbers = response.get('phoneNumbers', [])

        if phone_numbers:
            return phone_numbers[0]['value']
        else:
            return None
    except Exception as e:
        print('Failed to fetch phone number:', str(e))
        return None
