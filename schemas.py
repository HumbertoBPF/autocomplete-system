from marshmallow import Schema, fields


class MeaningSchema(Schema):
    text = fields.Str()


class WordSchema(Schema):
    word = fields.Str()
    meanings = fields.Nested(MeaningSchema(), many=True)
