import array
import os
import json
from fastapi import FastAPI, HTTPException, Depends, Query
from fastapi.responses import RedirectResponse
from google.auth.transport.requests import Request
from pydantic import BaseModel
from typing import Optional, List
from dotenv import load_dotenv
from google_auth_oauthlib.flow import Flow
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

# Load environment variables from .env file
load_dotenv()

app = FastAPI()

# Retrieve environment variables
GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")
GOOGLE_REDIRECT_URI = os.getenv("GOOGLE_REDIRECT_URI")
GOOGLE_SCOPES = os.getenv("GOOGLE_SCOPES").split(',')

# OAuth flow initialization
flow = Flow.from_client_config({
    "web": {
        "client_id": GOOGLE_CLIENT_ID,
        "client_secret": GOOGLE_CLIENT_SECRET,
        "redirect_uris": [GOOGLE_REDIRECT_URI],
        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
        "token_uri": "https://oauth2.googleapis.com/token"
    }
}, scopes=GOOGLE_SCOPES, redirect_uri=GOOGLE_REDIRECT_URI)


class Event(BaseModel):
    summary: str
    description: Optional[str] = None
    start: dict
    end: dict
    location: Optional[str] = None
    attendees: Optional[List[str]] = None


# In-memory storage for user credentials
user_creds = {}


@app.get("/auth/login")
def login():
    # Redirect user to Google's OAuth2 login page
    authorization_url, state = flow.authorization_url(access_type='offline', include_granted_scopes='true')
    return RedirectResponse(url=authorization_url)


@app.get("/auth/redirect")
async def auth_redirect(code: str = Query(...)):
    # Exchange the authorization code for an access token
    flow.fetch_token(code=code)
    credentials = flow.credentials

    # # Save credentials to token.json
    # with open("token.json", "w") as token:
    #     token.write(credentials.to_json())

    # Save credentials in-memory, for single user only
    user_creds['token'] = credentials.to_json()

    return {"message": "Authentication successful", "token": credentials.token}


def get_calendar_service():
    # Returns an authorized Google Calendar API service
    if 'token' not in user_creds:
        raise HTTPException(status_code=401, detail="User not authenticated")

    creds = Credentials.from_authorized_user_info(json.loads(user_creds['token']))

    # Refresh token if expired
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())

    service = build('calendar', 'v3', credentials=creds)
    return service


@app.get("/events")
async def get_events():
    # Get list of events in the user's primary calendar
    service = get_calendar_service()
    events_res = service.events().list(calendarId='primary', maxResults=10).execute()
    return events_res.get('items', [])


@app.post("/events")
async def create_event(event: Event):
    # Create an event in the user's primary calendar
    service = get_calendar_service()
    event_payload = {
        'summary': event.summary,
        'location': event.location,
        'description': event.description,
        'start': event.start,
        'end': event.end,
        'attendees': [{'email': email} for email in event.attendees] if event.attendees else [],
        'conferenceData': {
            'createRequest': {
                'conferenceSolutionKey': {
                    'type': 'hangoutsMeet'
                },
                'requestId': '1'  # Some random unique string
            }
        }
    }

    created_event = service.events().insert(calendarId='primary',
                                            body=event_payload, conferenceDataVersion=1).execute()
    return {"event": created_event}


# json payload for creating event, in route '/events', POST request
# {
#     "summary": "Project Kickoff Meeting",
#     "description": "Discussing the new project with the team.",
#     "start": {
#         "dateTime": "2024-09-15T09:00:00-07:00",
#         "timeZone": "America/Los_Angeles"
#     },
#     "end": {
#         "dateTime": "2024-09-15T10:00:00-07:00",
#         "timeZone": "America/Los_Angeles"
#     },
#     "location": "Google Meet",
#     "attendees": ["raselhasan.cse11@gmail.com"],
# }
#
# /events?attendees=["raselhasan.cse11@gmail.com"]
