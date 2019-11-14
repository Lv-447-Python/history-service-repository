"""Module for history marshmallow schema."""
from history_service import marshmallow
from history_service.models.history_model import History


class HistorySchema(marshmallow.ModelSchema):
    """History marshmallow schema."""
    class Meta:
        model = History

