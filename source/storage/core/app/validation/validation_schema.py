from marshmallow import Schema, fields, validate, INCLUDE


class AddingUrlsSchema(Schema):
    user_id = fields.Integer(required=True)
    links = fields.List(fields.Url(), required=True)
    unknown = INCLUDE


class NextUrlsSchema(Schema):
    user_id = fields.Integer(required=True)
    quantity = fields.Integer(required=True)
    unknown = INCLUDE

class StoreConfigSchema(Schema):
    user_id = fields.Integer(required=True)
    specificTag = fields.List(fields.String(), required=True)
    samePage = fields.Boolean(required=True)
    memoryLimit = fields.Integer(required=True)
    unknown = INCLUDE

class RetrieveConfigSchema(Schema):
    user_id = fields.Integer(required=True)
    unknown = INCLUDE

class UsernameAccessSchema(Schema):
    user_id = fields.Integer(required=True)
    unknown = INCLUDE

class ParsedDataSchema(Schema):
    user_id = fields.Integer(required=True)
    content = fields.Dict(keys=fields.String(), values=fields.List(fields.String()), required=True)
    unknown = INCLUDE