from app.config import app, db, NextLinks, VisitedLinks, Configuration
from flask import jsonify

def get_next_links(request):
    json_resp = request.get_json('json_resp')

    db.session.begin_nested()
    db.session.execute('LOCK TABLE next_links IN ACCESS EXCLUSIVE MODE;')

    next_link_db_resp = NextLinks.query.limit(int(json_resp["quantity"])).all()

    dict_next_url = dict()
    dict_next_url["urls"] = []
    for el in next_link_db_resp:
        dict_next_url["urls"].append(el.url_site)
        db.session.delete(el)

    db.session.commit()

    db.session.execute('LOCK TABLE visited_links IN ACCESS EXCLUSIVE MODE;')
    for el in next_link_db_resp:
        db.session.add(VisitedLinks(url_site=el.url_site))

    db.session.commit()

    db.session.commit()

    return dict_next_url


def add_link_to_db(request):
    links = request.get_json(force=True)
    json_links = links["links"]

    for link in json_links:
        try:
            db.session.add(NextLinks(url_site=link))
            db.session.commit()
        except (TypeError):
            db.session.rollback()

    return jsonify({"success": "True"})