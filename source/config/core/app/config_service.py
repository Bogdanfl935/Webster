import json
import requests
from app.constants import endpoint_constants

def add_config_to_db(request):
    text = request.get_json()

    specific_tag = ["a"]
    stay_on_same_page = False if "same-page" not in text else text["same-page"]
    storage_limit = 100 if "storage-limit" not in text else text["storage-limit"]

    if "specific-tag" in text.keys():
        specific_tag.extend(text["specific-tag"])

    config_json = json.dumps(
        {"specific-tag": specific_tag, "same-page": stay_on_same_page, "storage-limit": storage_limit})

    post_to_db = requests.post(url=f'{endpoint_constants.STORAGE_MS_URL}{endpoint_constants.STORE_CONFIGURATION}',
                               data=config_json, headers={'Content-type': 'application/json'})

    return config_json

def retr_config_from_db(request, type_conf):
    recv_data_json = request.get_json()

    retr_config_req = json.dumps({"user": "george"})

    from_db_resp = requests.post(
        url=f'{endpoint_constants.STORAGE_MS_URL}{endpoint_constants.RETRIEVE_CONFIGURATION_DB}', data=retr_config_req,
        headers={'Content-type': 'application/json'})
    from_db_resp_json = from_db_resp.json()

    resp_json = dict()

    if type_conf == "crawler":
        resp_json["memoryLimit"] = from_db_resp_json["memoryLimit"]
        resp_json["same-page"] = from_db_resp_json["same-page"]
    elif type_conf == "parser":
        resp_json["specific-tag"] = from_db_resp_json["specific-tag"]

    return resp_json
