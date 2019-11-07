from marshmallow import Schema, fields, post_load
from history_service.models.history_model import History


class HistorySchema(Schema):
    file_id = fields.Int()
    filter_id = fields.Int()
    user_id = fields.Int()
    rows_id = fields.Str()
    filter_date = fields.DateTime(dump_only=True)

    @post_load
    def create_filter_object(self, history_data, **kwargs):
        return History(**history_data)