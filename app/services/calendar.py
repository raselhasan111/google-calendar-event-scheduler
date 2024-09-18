import json
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from fastapi import HTTPException

user_creds = {}


def get_calendar_service():
    if 'token' not in user_creds:
        raise HTTPException(status_code=401, detail='User not authenticated')

    creds = Credentials.from_authorized_user_info(json.loads(user_creds['token']))

    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())

    return build('calendar', 'v3', credentials=creds)
