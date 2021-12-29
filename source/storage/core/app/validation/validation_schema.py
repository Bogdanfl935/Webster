from marshmallow import Schema, fields, INCLUDE


class UrlInsertionSchema(Schema):
    username = fields.Email(required=True)
    urls = fields.List(fields.Url(), required=True)
    unknown = INCLUDE

class UrlUpdateSchema(Schema):
    username = fields.Email(required=True)
    urls = fields.List(fields.Url(), required=True)
    visited = fields.Boolean(required=True)
    unknown = INCLUDE


class UrlRetrievalSchema(Schema):
    username = fields.Email(required=True)
    quantity = fields.Integer(required=True)
    unknown = INCLUDE


class UsernameAccessSchema(Schema):
    username = fields.Email(required=True)
    unknown = INCLUDE


class ParsedContentInsertionSchema(Schema):
    username = fields.Email(required=True)
    tag = fields.String(required=True)
    content = fields.String(required=True)
    unknown = INCLUDE


class ParsedImageInsertionSchema(Schema):
    username = fields.Email(required=True)
    extension = fields.String(required=True)
    content = fields.String(required=True)
    unknown = INCLUDE


class ParsedDataDeletionSchema(Schema):
    username = fields.Email(required=True)
    id = fields.Integer(required=True)
    unknown = INCLUDE