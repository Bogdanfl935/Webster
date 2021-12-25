from app.config.config import db, ParsedContent
from flask import jsonify, request
import psycopg2

def get_content_from_db():
    user_id = int(request.args.get("user_id"))

    db_resp = db.session.query(ParsedContent.user_id, ParsedContent.tag, ParsedContent.content).filter(ParsedContent.user_id == user_id)

    resp_json = dict()

    resp_json["content"] = dict()

    for el in db_resp:
        resp_json["user_id"] = el[0]
        if el[1] not in resp_json["content"].keys():
            resp_json["content"][el[1]] = [el[2].decode('utf-8')]
        else:
            resp_json["content"][el[1]].append(el[2].decode('utf-8'))

    return jsonify(resp_json)

def add_new_content_to_db():
    config_json = request.get_json(force=True)

    user_id = config_json["user_id"]
    content = config_json["content"]

    for tag in content:
        for i in range(len(content[tag])):
            db.session.add(ParsedContent(user_id=user_id, tag=tag, content=content[tag][i].encode('utf-8')))

    db.session.commit()

    return jsonify({"success": "True"})