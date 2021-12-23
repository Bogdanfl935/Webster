from app.config.config import db, ParsedUrls, VisitedUrls
from flask import jsonify, abort, make_response
from http import HTTPStatus


def get_next_links(request):
    json_resp = request.get_json('json_resp')

    db.session.begin_nested()
    db.session.execute('LOCK TABLE parsed_urls IN ACCESS EXCLUSIVE MODE;')

    next_link_db_resp = ParsedUrls.query.limit(int(json_resp["quantity"])).all()

    dict_next_url = dict()
    dict_next_url["urls"] = []
    for el in next_link_db_resp:
        dict_next_url["urls"].append(el.url)
        db.session.delete(el)

    db.session.commit()

    db.session.execute('LOCK TABLE visited_urls IN ACCESS EXCLUSIVE MODE;')
    for el in next_link_db_resp:
        db.session.add(VisitedUrls(url=el.url, user_id = el.user_id))

    db.session.commit()

    db.session.commit()

    return jsonify(dict_next_url)

def add_link_to_db(request):
    links = request.get_json(force=True)
    json_links = links["links"]
    json_user_id = int(links["user_id"])

    for link in json_links:
        try:
            db.session.add(ParsedUrls(url=link, user_id=json_user_id))
            db.session.commit()
        except (TypeError):
            db.session.rollback()

    return jsonify({"success": "True"})