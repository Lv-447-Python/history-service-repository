from marshmallow import Schema, fields


class FilterSchema(Schema):
    filter_data = fields.Raw(required=True)
    filter_id = fields.Integer(dump_only=True)
