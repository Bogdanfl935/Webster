from marshmallow import Schema, fields, validate, INCLUDE


class MemoryUsageSchema(Schema):
    username = fields.Email(required=True)
    memoryUsage = fields.Integer(required=True, validate=validate.Range(min=0))
    unknown = INCLUDE


class UsernameAccessSchema(Schema):
    username = fields.Email(required=True)
    unknown = INCLUDE


class ConcurrentWritingSchema(Schema):
    username = fields.Email(required=True)
    active = fields.Boolean(required=True)
    unknown = INCLUDE


class ConcurrentContinuationWritingSchema(Schema):
    username = fields.Email(required=True)
    continuation = fields.Boolean(required=True)
    unknown = INCLUDE


class LastUrlSchema(Schema):
    username = fields.Email(required=True)
    lastUrl = fields.Url(required=True)
    unknown = INCLUDE

class TagDetailsSchema(Schema):
    tag = fields.String(required=True)
    memoryUsage = fields.Integer(required=True, validate=validate.Range(min=0))
    unknown = INCLUDE

class ParsedContentSchema(Schema):
    url = fields.Url(required=True)
    content = fields.List(fields.Nested(TagDetailsSchema, required=True), required=True)
    unknown = INCLUDE

class LastParsedSchema(Schema):
    username = fields.Email(required=True)
    lastParsed = fields.Nested(ParsedContentSchema, required=True)
    unknown = INCLUDE


