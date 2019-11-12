from history_service import marshmallow
from history_service.models.filter_model import Filter


class FilterSchema(marshmallow.ModelSchema):
    class Meta:
        model = Filter
