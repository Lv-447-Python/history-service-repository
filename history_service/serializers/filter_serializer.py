from marshmallow import Schema, fields, post_load
from history_service.models.filter_model import Filter


class FilterSchema(Schema):
    filter_id = fields.Integer(dump_only=True)
    filter_data = fields.Str(required=True)

    @post_load
    def create_filter_object(self, filter_data, **kwargs):
        return Filter(**filter_data)
