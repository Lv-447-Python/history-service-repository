"""Module for filter marshmallow schema."""
from history_service import MARSHMALLOW
from history_service.models.filter_model import Filter


class FilterSchema(MARSHMALLOW.ModelSchema):
    """Filter marshmallow schema."""
    class Meta:
        model = Filter
