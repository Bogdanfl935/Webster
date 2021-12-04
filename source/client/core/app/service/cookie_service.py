from flask import Response
from app.constants import browser_constants

def remove_cookies(response: Response):
    response.delete_cookie(browser_constants.ACCESS_TOKEN_COOKIE)
    response.delete_cookie(browser_constants.REFRESH_TOKEN_COOKIE)

def set_access_token_cookie(response: Response, access_token: str, token_type: str):
    response.set_cookie(key=browser_constants.ACCESS_TOKEN_COOKIE,
                        value=f"{token_type} {access_token}",
                        max_age=browser_constants.ACCESS_TOKEN_COOKIE_EXPIRY_SECONDS)


def set_refresh_token_cookie(response: Response, refresh_token: str, keep_signed_in: bool):
    cookie_age = browser_constants.REFRESH_TOKEN_COOKIE_LONG_EXPIRY_SECONDS if keep_signed_in is True \
        else browser_constants.REFRESH_TOKEN_COOKIE_SHORT_EXPIRY_SECONDS
        
    response.set_cookie(key=browser_constants.REFRESH_TOKEN_COOKIE,
                        value=refresh_token,
                        max_age=cookie_age)
