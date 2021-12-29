from marshmallow import Schema, fields, INCLUDE


class ParserConfigurationSchema(Schema):
    username = fields.Email(required=True)
    tag = fields.String(required=True)
    unknown = INCLUDE

class CrawlerConfigurationSchema(Schema):
    username = fields.Email(required=True)
    keyword = fields.String(required=True)
    active = fields.Boolean(required=True)
    unknown = INCLUDE


class UsernameAccessSchema(Schema):
    username = fields.Email(required=True)
    unknown = INCLUDE