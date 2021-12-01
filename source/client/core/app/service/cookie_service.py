from flask import Response
from app.constants import browser_constants

def set_access_token_cookie(response: Response, access_token: str, token_type: str):
    response.set_cookie(key=browser_constants.ACCESS_TOKEN_COOKIE,
                        value=f"{token_type} {access_token}",
                        max_age=browser_constants.ACCESS_TOKEN_COOKIE_EXPIRY_SECONDS)


def set_refresh_token_cookie(response: Response, refresh_token: str):
    response.set_cookie(key=browser_constants.REFRESH_TOKEN_COOKIE,
                        value=refresh_token,
                        max_age=browser_constants.REFRESH_TOKEN_COOKIE_EXPIRY_SECONDS)
