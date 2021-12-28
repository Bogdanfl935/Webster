import json
import requests
from app.constants import endpoint_constants

def add_config_to_db(request):
    text = request.get_json()

    specific_tag = ["a"]
    stay_on_same_page = False if "samePage" not in text else text["samePage"]
    storage_limit = 100 if "memoryLimit" not in text else text["memoryLimit"]

    if "specificTag" in text.keys():
        specific_tag.extend(text["specificTag"])

    config_json = json.dumps(
        {"specificTag": specific_tag, "samePage": stay_on_same_page, "memoryLimit": storage_limit})

    post_to_db = requests.post(url=f'{endpoint_constants.STORAGE_MS_URL}{endpoint_constants.STORE_CONFIGURATION}',
                               data=config_json, headers={'Content-type': 'application/json'})

    return config_json

def retr_config_from_db(request, type_conf):
    recv_data_json = request.get_json()

    retr_config_req = json.dumps({"user_id": "2121"})

    from_db_resp = requests.post(
        url=f'{endpoint_constants.STORAGE_MS_URL}{endpoint_constants.RETRIEVE_CONFIGURATION_DB}', data=retr_config_req,
        headers={'Content-type': 'application/json'})
    from_db_resp_json = from_db_resp.json()

    resp_json = dict()

    if type_conf == "crawler":
        resp_json["memoryLimit"] = from_db_resp_json["memoryLimit"]
        resp_json["samePage"] = from_db_resp_json["samePage"]
    elif type_conf == "parser":
        resp_json["specificTag"] = from_db_resp_json["specificTag"]

    return resp_json
