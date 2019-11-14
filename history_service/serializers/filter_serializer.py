"""Module for filter marshmallow schema."""
from history_service import marshmallow
from history_service.models.filter_model import Filter


class FilterSchema(marshmallow.ModelSchema):
    """Filter marshmallow schema."""
    class Meta:
        model = Filter
