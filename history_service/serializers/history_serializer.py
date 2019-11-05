from marshmallow import Schema, fields
from history_service.models.history_model import History


class HistorySchema(Schema):
    file_id = fields.Int()
    filter_id = fields.Int()
    user_id = fields.Int()
    rows_id = fields.Raw()
    filter_date = fields.DateTime(dump_only=True)
