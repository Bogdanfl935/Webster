from app.constants import serialization_constants, sql_models
from app.services import persistence_service
from app.services.foreign_key_mapping_service import fetch_user_id, fetch_source_id
from flask import request, Response, make_response, jsonify
from http import HTTPStatus
from sqlalchemy.sql import func
import base64
from urllib.parse import urlparse


def get_content_private():
    user_id = fetch_user_id(request.args.get(serialization_constants.USERNAME_KEY))

    query_func = lambda session: session.query(func.count(sql_models.ParsedContent.tag), sql_models.ParsedUrl.url) \
        .join(sql_models.ParsedUrl).filter(sql_models.ParsedContent.user_id == user_id).group_by(
        sql_models.ParsedUrl.url).order_by(func.count(sql_models.ParsedContent.tag).desc()).limit(10)

    records = persistence_service.query(query_func)
    response = [{"url": url, "count": count} for (count, url) in records]

    return jsonify(response)


def get_content_public():
    query_func = lambda session: session.query(func.count(sql_models.ParsedContent.tag), sql_models.ParsedUrl.url) \
        .join(sql_models.ParsedUrl).group_by(sql_models.ParsedUrl.url).order_by(
        func.count(sql_models.ParsedContent.tag).desc()).limit(10)

    records = persistence_service.query(query_func)
    response = [{"url": url, "count": count} for (count, url) in records]

    return jsonify(response)


def get_most_tags_private():
    user_id = fetch_user_id(request.args.get(serialization_constants.USERNAME_KEY))

    query_func = lambda session: session.query(func.count(sql_models.ParsedContent.tag), sql_models.ParsedUrl.url) \
        .join(sql_models.ParsedUrl).filter(sql_models.ParsedContent.user_id == user_id).group_by(
        sql_models.ParsedUrl.url).order_by(func.count(sql_models.ParsedContent.tag).desc()).limit(10)

    records = persistence_service.query(query_func)

    return records[0][0]


def get_most_tags_public():
    query_func = lambda session: session.query(func.count(sql_models.ParsedContent.tag), sql_models.ParsedUrl.url) \
        .join(sql_models.ParsedUrl).group_by(sql_models.ParsedUrl.url).order_by(
        func.count(sql_models.ParsedContent.tag).desc()).limit(10)

    records = persistence_service.query(query_func)

    return records[0][0]


def get_most_tags_source_private():
    user_id = fetch_user_id(request.args.get(serialization_constants.USERNAME_KEY))

    query_func = lambda session: session.query(func.count(sql_models.ParsedContent.tag), sql_models.ParsedUrl.url) \
        .join(sql_models.ParsedUrl).filter(sql_models.ParsedContent.user_id == user_id).group_by(
        sql_models.ParsedUrl.url).order_by(func.count(sql_models.ParsedContent.tag).desc()).limit(10)

    records = persistence_service.query(query_func)

    return records[0][1]


def get_most_tags_source_public():
    query_func = lambda session: session.query(func.count(sql_models.ParsedContent.tag), sql_models.ParsedUrl.url) \
        .join(sql_models.ParsedUrl).group_by(sql_models.ParsedUrl.url).order_by(
        func.count(sql_models.ParsedContent.tag).desc()).limit(10)

    records = persistence_service.query(query_func)

    return records[0][1]


def get_total_parsed_urls_private():
    user_id = fetch_user_id(request.args.get(serialization_constants.USERNAME_KEY))

    query_func = lambda session: session.query(func.count(sql_models.ParsedUrl.url)). \
        filter(sql_models.ParsedUrl.user_id == user_id).scalar()

    records = persistence_service.query(query_func)

    return records


def get_total_parsed_urls_public():
    query_func = lambda session: session.query(func.count(sql_models.ParsedUrl.url)).scalar()

    records = persistence_service.query(query_func)

    return records
