def extract_errors_response(response: dict) -> str:
    formatted_errors_list = [error_dict["defaultMessage"] for error_dict in response["errors"]]
    return "\n".join(formatted_errors_list)

def extract_message_response(response: dict) -> str:
    return response["message"]

def extract_confirmation_token_response(response: dict) -> str:
    return response["confirmationToken"]