"""Module for history marshmallow schema."""
from history_service import MARSHMALLOW
from history_service.models.history_model import History


class HistorySchema(MARSHMALLOW.ModelSchema):
    """History marshmallow schema."""
    class Meta:
        """Meta class for History marshmallow schema."""
        model = History
