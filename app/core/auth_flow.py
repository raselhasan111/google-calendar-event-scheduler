from google_auth_oauthlib.flow import Flow
from app.core.config import GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET, GOOGLE_REDIRECT_URI, GOOGLE_SCOPES


def get_google_flow():
    return Flow.from_client_config({
        'web': {
            'client_id': GOOGLE_CLIENT_ID,
            'client_secret': GOOGLE_CLIENT_SECRET,
            'redirect_uris': [GOOGLE_REDIRECT_URI],
            'auth_uri': 'https://accounts.google.com/o/oauth2/auth',
            'token_uri': 'https://oauth2.googleapis.com/token'
        }
    }, scopes=GOOGLE_SCOPES, redirect_uri=GOOGLE_REDIRECT_URI)
