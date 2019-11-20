"""Module for filter resource."""
import json
from flask import request, make_response, jsonify
from flask_restful import Resource
from flask_api import status
from marshmallow.exceptions import ValidationError
from history_service import API
from history_service import APP
from history_service.models.filter_model import Filter
from history_service.serializers.filter_serializer import FilterSchema
from history_service.utils.utils import save_into_db, delete_from_db


def dump_filter_object(filter_object):
    """
    Method for filter object serialization.
    Args:
        filter_object:
            Any instance of Filter model class.
    Returns:
        Formatted data presentation.
    """
    filter_serializer = FilterSchema()
    filter_value = filter_serializer.dump(filter_object)
    filter_value['filter_data'] = json.loads(filter_value['filter_data'])
    return filter_value


def load_filter_object(filter_value):
    """
    Method for filter object deserialization and validation.
    Args:
        filter_value:
            Input dictionary.
    Returns:
        Filter model instance.
    """
    filter_serializer = FilterSchema()
    filter_object = filter_serializer.load(filter_value)
    return filter_object


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
        return make_response(jsonify(filters), status.HTTP_200_OK)

    def post(self):
        """
        Method for HTTP POST method working out. Used for creation filter resources.
        Returns:
            New filter in accordance to request and query status.
        """
        filter_value = request.get_json()
        try:
            filter_value['filter_data'] = json.dumps(filter_value['filter_data'])
        except KeyError as key_error:
            APP.logger.exception(key_error)
            return status.HTTP_400_BAD_REQUEST

        try:
            filter_object = load_filter_object(filter_value)
        except ValidationError as validation_error:
            APP.logger.exception(validation_error)
            return status.HTTP_400_BAD_REQUEST
        existing_filter = Filter.query.filter_by(filter_data=filter_object.filter_data).first()

        if not existing_filter:
            save_into_db(filter_object)
            new_filter = dump_filter_object(filter_object)
            return make_response(jsonify(new_filter), status.HTTP_201_CREATED)
        new_filter = dump_filter_object(existing_filter)
        return make_response(jsonify(new_filter), status.HTTP_201_CREATED)


class SingleFilterResource(Resource):
    """Single filter resource class."""

    def get(self, filter_id):
        """
        Method for HTTP GET method working out. Used for getting single filter resources.
        Returns:
            Filters in accordance to GET method arguments and query status.
        """
        filter_object = Filter.query.filter_by(filter_id=filter_id).first()
        if filter_object:
            filter_value = dump_filter_object(filter_object)
            return make_response(jsonify(filter_value), status.HTTP_200_OK)
        return status.HTTP_400_BAD_REQUEST

    def delete(self, filter_id):
        """
        Method for HTTP DELETE method working out. Used for deleting single filter resources.
        Returns:
            Deleted filter in accordance to DELETE method arguments and query status.
        """
        filter_object = Filter.query.filter_by(filter_id=filter_id).first()
        if filter_object:
            delete_from_db(filter_object)
            filter_value = dump_filter_object(filter_object)
            return make_response(jsonify(filter_value), status.HTTP_200_OK)
        return status.HTTP_400_BAD_REQUEST


API.add_resource(FiltersResource, '/filter')
API.add_resource(SingleFilterResource, '/filter/<int:filter_id>')
