from app.config import app, db, ParsedUrls, VisitedUrls, Configuration
from flask import jsonify
from flask import abort
from werkzeug.exceptions import HTTPException
import validators


def get_next_links(request):
    json_resp = request.get_json('json_resp')

    db.session.begin_nested()
    db.session.execute('LOCK TABLE parsed_urls IN ACCESS EXCLUSIVE MODE;')

    next_link_db_resp = ParsedUrls.query.limit(int(json_resp["quantity"])).all()

    dict_next_url = dict()
    dict_next_url["urls"] = []
    for el in next_link_db_resp:
        validate_url(el.url)
        dict_next_url["urls"].append(el.url)
        db.session.delete(el)

    db.session.commit()

    db.session.execute('LOCK TABLE visited_urls IN ACCESS EXCLUSIVE MODE;')
    for el in next_link_db_resp:
        validate_url(el.url)
        db.session.add(VisitedUrls(url=el.url))

    db.session.commit()

    db.session.commit()

    return dict_next_url


def add_link_to_db(request):
    links = request.get_json(force=True)
    json_links = links["links"]

    for link in json_links:
        try:
            db.session.add(ParsedUrls(url=link))
            db.session.commit()
        except (TypeError):
            db.session.rollback()

    return jsonify({"success": "True"})

def validate_url(url):
    if not validators.url(url):
        abort(400, description={"fieldName": "urls", "errorMessage": f"url not properly formated"})