"""Module for filter resource."""
from flask import make_response, jsonify
from flask_restful import Resource
from flask_api import status
from history_service import API
from history_service import LOGGER
from history_service.models.filter_model import Filter
from history_service.utils.utils import dump_filter_object


class FiltersResource(Resource):
    """Filters resource class."""

    def get(self):
        """
        Method for HTTP GET method working out. Used for getting all filters resources.
        Returns:
            All filters.
        """
        filter_objects = Filter.query.all()
        filters = list(map(dump_filter_object, filter_objects))
        LOGGER.info('Successful request to FilterResource')
        return make_response(jsonify(filters), status.HTTP_200_OK)


class SingleFilterResource(Resource):
    """Single filter resource class."""

    def get(self, filter_id):
        """
        Method for HTTP GET method working out. Used for getting single filter resources.
        Args:
            filter_id:
                Filter identifier.
        Returns:
            Filters in accordance to GET method arguments and query status.
        """
        filter_object = Filter.query.filter_by(filter_id=filter_id).first()
        if filter_object:
            filter_value = dump_filter_object(filter_object)
            LOGGER.info('Successful request to SingleFilterResource')
            return make_response(jsonify(filter_value), status.HTTP_200_OK)
        LOGGER.error('Invalid filter id parameter')
        return make_response({}, status.HTTP_400_BAD_REQUEST)


API.add_resource(FiltersResource, '/filter')
API.add_resource(SingleFilterResource, '/filter/<int:filter_id>')
