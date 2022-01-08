from marshmallow import Schema, fields, INCLUDE

class StartCrawlerSchema(Schema):
    username = fields.Email(required=True)
    startUrl = fields.Url(required=True)
    unknown = INCLUDE
    
class UsernameAccessSchema(Schema):
    username = fields.Email(required=True)
    unknown = INCLUDE