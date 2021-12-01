def extract_errors_response(response: dict) -> str:
    formatted_errors_list = [error_dict["defaultMessage"] for error_dict in response["errors"]]
    return "\n".join(formatted_errors_list)

def extract_message_response(response: dict) -> str:
    return response["message"]

def extract_confirmation_token_response(response: dict) -> str:
    return response["confirmationToken"]

def extract_access_token_response(response: dict) -> tuple:
    return response["accessToken"], response["refreshToken"], response["type"]

def extract_refreshment_response(response: dict) -> tuple:
    return response["accessToken"], response["type"], response["subject"]

def extract_subject_response(response: dict) -> str:
    return response["subject"]