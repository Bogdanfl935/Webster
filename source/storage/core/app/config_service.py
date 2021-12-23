from app.config import app, db, ParsedUrls, VisitedUrls, Configuration
from flask import jsonify

def get_config_from_db(request):
    json_resp = request.get_json()

    config_db_resp = Configuration.query.all()

    resp_json = dict()

    for el in config_db_resp:
        if el.key == "specific-tag":
            if el.key in resp_json.keys():
                resp_json[el.key].append(el.value)
            else:
                resp_json[el.key] = [el.value]
        else:
            resp_json[el.key] = el.value

    return jsonify(resp_json)

def add_new_config_to_db(request):
    config_json = request.get_json(force=True)

    user_id = config_json["user_id"]
    specific_tag = config_json["specific-tag"]
    same_page = config_json["same-page"]
    storage_limit = config_json["memoryLimit"]

    for el in specific_tag:
        db.session.add(Configuration(key="specific-tag", value=el, user_id=user_id))

    db.session.add(Configuration(key="same-page", value=same_page, user_id=user_id))
    db.session.add(Configuration(key="memoryLimit", value=storage_limit, user_id=user_id))

    db.session.commit()

    return jsonify({"success": "True"})