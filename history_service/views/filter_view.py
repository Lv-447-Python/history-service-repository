"""Module for filter resource."""
import json
from flask import request
from flask_restful import Resource
from flask_api import status
from marshmallow.exceptions import ValidationError
from history_service import API
from history_service import APP
from history_service.models.filter_model import Filter
from history_service.serializers.filter_serializer import FilterSchema
from history_service.utils.utils import jsonify_data, save_into_db, delete_from_db


class FilterResource(Resource):
    """Filter resource class."""

    @staticmethod
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

    @staticmethod
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

    def get(self):
        """
        Method for HTTP GET method working out. Used for getting filter resources.
        Returns:
            Filters in accordance to GET method arguments, errors and query status.
        """
        filter_id = request.args.get('filter_id', type=int)
        if filter_id:
            filter_object = Filter.query.filter_by(filter_id=filter_id).first()
            if filter_object:
                filter_value = FilterResource.dump_filter_object(filter_object)
                return jsonify_data(filter_value, '', status.HTTP_200_OK)
        return jsonify_data({}, 'Filter method get: invalid input data!',
                            status.HTTP_400_BAD_REQUEST)

    def post(self):
        """
        Method for HTTP POST method working out. Used for creation filter resources.
        Returns:
            New filter in accordance to request, errors and query status.
        """
        filter_value = request.get_json()
        try:
            filter_value['filter_data'] = json.dumps(filter_value['filter_data'])
        except KeyError as key_error:
            APP.logger.exception(key_error)
            return jsonify_data({}, 'Filter method post: invalid input json!',
                                status.HTTP_400_BAD_REQUEST)

        try:
            filter_object = FilterResource.load_filter_object(filter_value)
        except ValidationError as validation_error:
            APP.logger.exception(validation_error)
            return jsonify_data({}, 'Filter method post: serialization error!',
                                status.HTTP_400_BAD_REQUEST)
        existing_filter = Filter.query.filter_by(filter_data=filter_object.filter_data).first()

        if not existing_filter:
            save_into_db(filter_object)
            new_filter = FilterResource.dump_filter_object(filter_object)
            return jsonify_data(new_filter, '', status.HTTP_200_OK)
        new_filter = FilterResource.dump_filter_object(existing_filter)
        return jsonify_data(new_filter, '', status.HTTP_200_OK)

    def delete(self):
        """
        Method for HTTP DELETE method working out. Used for deleting filter resources.
        Returns:
            Deleted filter in accordance to DELETE method arguments, errors and query status.
        """
        filter_id = request.args.get('filter_id', type=int)
        if filter_id:
            filter_object = Filter.query.filter_by(filter_id=filter_id).first()
            if filter_object:
                delete_from_db(filter_object)
                filter_value = FilterResource.dump_filter_object(filter_object)
                return jsonify_data(filter_value, '', status.HTTP_200_OK)
        return jsonify_data({}, 'Filter method delete: invalid input data!',
                            status.HTTP_400_BAD_REQUEST)


API.add_resource(FilterResource, '/filter')
