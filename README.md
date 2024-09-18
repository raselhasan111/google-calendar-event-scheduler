# Google Calendar Event Scheduler
#### A FastAPI-based application that allows users to schedule and manage events using the Google Calendar API. The app integrates Google OAuth for authentication and enables event creation and retrieval from a user's Google Calendar.

## Features
* Google OAuth2 for user authentication.
* Fetch upcoming events from the user's primary Google Calendar.
* Create new events on the user's Google Calendar.
* In-memory token storage for authenticated users (single-user session), specially for project simplicity.

## Project Structure

```plaintext
google-calendar-event-scheduler/
│
├── app/
│   ├── api/
│   │   ├── auth.py            # Handles authentication routes
│   │   ├── events.py          # Handles event-related routes
│   │   └── __init__.py        # Imports FastAPI routes from different modules
│   ├── core/
│   │   ├── config.py          # Configuration for environment variables and settings
│   │   └── auth_flow.py       # Google OAuth flow setup and helper functions
│   ├── models/
│   │   ├── event.py           # Pydantic models for request/response schemas
│   │   └── __init__.py        # Imports all models
│   ├── services/
│   │   ├── calendar.py        # Calendar service interactions
│   │   └── __init__.py
│   ├── __init__.py            # Initialize FastAPI app
│   └── main.py                # Entry point for the application
├── .env                       # Environment variables, ignored from git tracking
├── .env.example               # Environment variables example
└── requirements.txt           # Dependencies
```

## Pre-requisites
* Python 3.12
* A Google Cloud project with Google Calendar API and OAuth credentials.
* Virtual environment (venv)

## Setting up Google OAuth
1. Go to the Google Cloud Console.
2. Create a project and enable the Google Calendar API.
3. **Set-up OAuth 2.0 credentials:**
Authorized redirect URIs should match the one used in the .env file.
4. Download the OAuth client credentials and place them in your .env file.

## Environment Variables
* Create a *.env* file in the root directory with the following contents same as *.env.example* file:

```commandline
GOOGLE_CLIENT_ID=your-client-id
GOOGLE_CLIENT_SECRET=your-client-secret
GOOGLE_REDIRECT_URI=http://localhost:8000/auth/redirect
GOOGLE_SCOPES=https://www.googleapis.com/auth/calendar
```

## Installation
### **Clone the repository:**

```commandline
git clone https://github.com/raselhasan111/google-calendar-event-scheduler.git
cd google-calendar-event-scheduler
```

### **Create and activate a virtual environment:**

```commandline
python3 -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```

### **Install dependencies:**

```commandline
pip install -r requirements.txt
```

**And set up your environment variables in .env (as shown above).**

## Running the Application
### Start the FastAPI app using Uvicorn:
```commandline
uvicorn app.main:app --reload
```

**The app will be running at *http://127.0.0.1:8000.***

### Endpoints
* Login with Google OAuth
```commandline
Endpoint: /auth/login
Method: GET
Description: Redirects the user to Google's OAuth2 login page.
```

* Handle OAuth Redirect
```commandline
Endpoint: /auth/redirect
Method: GET
Description: Handles the OAuth2 callback and saves the access token.
```

* Get Events
```commandline
Endpoint: /events
Method: GET
Description: Fetches up to 10 upcoming events from the user's Google Calendar.
```

* Create Event
```commandline
Endpoint: /events
Method: POST
Description: Creates a new event in the user's Google Calendar.
```

**Sample Request:**

```json
{
    "summary": "Project Kickoff Meeting",
    "description": "Discussing the new project with the team.",
    "start": {
        "dateTime": "2024-10-15T09:00:00-07:00",
        "timeZone": "America/Los_Angeles"
    },
    "end": {
        "dateTime": "2024-10-15T10:00:00-07:00",
        "timeZone": "America/Los_Angeles"
    },
    "location": "Google Meet",
    "attendees": ["email@example.com"]
}
```
**Open *http://127.0.0.1:8000/docs* to test endpoints with swagger.**

## License
This project is licensed under the *MIT License*. See the LICENSE file for details.