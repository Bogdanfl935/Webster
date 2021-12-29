from marshmallow import Schema, fields, INCLUDE


class ParserSchema(Schema):
    username = fields.Email(required=True)
    url = fields.Url(required=True)
    headers = fields.String(required=True)
    content = fields.String(required=True)
    unknown = INCLUDE
    
class UsernameAccessSchema(Schema):
    username = fields.Email(required=True)
    unknown = INCLUDE