from fastapi import APIRouter
from fastapi.responses import RedirectResponse
from fastapi import Query
from app.core.auth_flow import get_google_flow
from app.services.calendar import user_creds

router = APIRouter()


@router.get("/login")
def login():
    flow = get_google_flow()
    authorization_url, state = flow.authorization_url(access_type='offline', include_granted_scopes='true')
    return RedirectResponse(url=authorization_url)


@router.get("/redirect")
async def auth_redirect(code: str = Query(...)):
    flow = get_google_flow()
    flow.fetch_token(code=code)
    credentials = flow.credentials
    user_creds['token'] = credentials.to_json()
    return {"message": "Authentication successful", "token": credentials.token}
