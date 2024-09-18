from fastapi import APIRouter
from app.models.event import Event
from app.services.calendar import get_calendar_service

router = APIRouter()


@router.get("/events")
async def get_events():
    service = get_calendar_service()
    events_res = service.events().list(calendarId='primary', maxResults=10).execute()
    return events_res.get('items', [])


@router.post("/events")
async def create_event(event: Event):
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
                'requestId': '1'
            }
        }
    }
    created_event = service.events().insert(calendarId='primary', body=event_payload, conferenceDataVersion=1).execute()
    return {"event": created_event}

# Example json payload for creating event
# GET request in ('/calendar/events') route
# {
#     "summary": "Project Kickoff Meeting",
#     "description": "Discussing the new project with the team.",
#     "start": {
#         "dateTime": "2024-10-15T09:00:00-07:00",
#         "timeZone": "America/Los_Angeles"
#     },
#     "end": {
#         "dateTime": "2024-10-15T10:00:00-07:00",
#         "timeZone": "America/Los_Angeles"
#     },
#     "location": "Google Meet",
#     "attendees": ["raselhasan.cse11@gmail.com"]
# }


