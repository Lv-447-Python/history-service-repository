from history_service import marshmallow
from history_service.models.history_model import History


class HistorySchema(marshmallow.ModelSchema):
    class Meta:
        model = History

