from marshmallow import Schema, fields, validate, INCLUDE


class AddConfigSchema(Schema):
    user_id = fields.Integer(required=True, validate=validate.Range(min=0))
    memoryLimit = fields.Integer(required=True, validate=validate.Range(min=0))
    specificTag = fields.List(fields.String(), required=True)
    samePage = fields.Boolean()
    unknown = INCLUDE


class RetriveConfigSchema(Schema):
    user_id = fields.Integer(required=True, validate=validate.Range(min=0))
    unknown = INCLUDE
