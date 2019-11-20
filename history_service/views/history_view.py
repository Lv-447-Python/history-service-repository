"""Module for history resource."""
import json
import requests
from flask import request, jsonify, make_response
from flask_restful import Resource
from flask_api import status
from marshmallow.exceptions import ValidationError
from history_service import API
from history_service import APP
from history_service.models.history_model import History
from history_service.serializers.history_serializer import HistorySchema
from history_service.utils.utils import save_into_db, delete_from_db


def dump_history_object(history_object):
    """
    Method for history object serialization.
    Args:
        history_object:
            Any instance of History model class.
    Returns:
        Formatted data presentation.
    """
    history_serializer = HistorySchema()
    history = history_serializer.dump(history_object)
    history['rows_id'] = json.loads(history['rows_id'])
    return history


def load_history_object(history):
    """
    Method for history object deserialization and validation.
    Args:
        history:
            Input dictionary.
    Returns:
        History model instance.
    """
    history_serializer = HistorySchema()
    history_object = history_serializer.load(history)
    return history_object


class HistoryResource(Resource):
    """History resource class."""

    def get(self):
        """
        Method for HTTP GET method working out. Used for getting all history resources.
        Returns:
            All history records.
        """
        history_objects = History.query.all()
        history = list(map(dump_history_object, history_objects))
        return make_response(jsonify(history), status.HTTP_200_OK)

    def post(self):
        """
        Method for HTTP POST method working out. Used for creation history resources.
        Returns:
            New history records in accordance to request and query status.
        """
        history_record = request.get_json()

        try:
            history = {
                'user_id': history_record['user_id'],
                'file_id': history_record['file_id'],
                'rows_id': json.dumps(history_record['rows_id'])
            }
            filter_value = {'filter_data': history_record['filter_data']}
        except KeyError as key_error:
            APP.logger.exception(key_error)
            return status.HTTP_400_BAD_REQUEST

        new_filter = requests.post('http://127.0.0.1:5000/filter', json=filter_value)
        response = new_filter.json()
        history['filter_id'] = response['filter_id']

        try:
            history_object = load_history_object(history)
        except ValidationError as validation_error:
            APP.logger.exception(validation_error)
            return status.HTTP_400_BAD_REQUEST

        existing_history_record = History.query.filter_by(
            user_id=history_object.user_id,
            file_id=history_object.file_id,
            filter_id=history_object.filter_id).first()

        if not existing_history_record:
            save_into_db(history_object)
            new_history = dump_history_object(history_object)
            return make_response(jsonify(new_history), status.HTTP_201_CREATED)

        return status.HTTP_400_BAD_REQUEST


class HistoryRecordResource(Resource):
    """History record resource class."""

    def get(self, user_id, file_id, filter_id):
        """
        Method for HTTP GET method working out. Used for getting history resources.
        Returns:
            History records in accordance to GET method arguments and query status.
        """
        print(user_id, file_id, filter_id)
        history_data = {
            'user_id': user_id,
            'file_id': file_id,
            'filter_id': filter_id
        }
        history_objects = History.query.filter_by(**history_data).all()
        if history_objects:
            history = list(map(dump_history_object, history_objects))
            return make_response(jsonify(history), status.HTTP_200_OK)
        return status.HTTP_400_BAD_REQUEST


class DeleteHistoryRecordResource(Resource):
    """Deleting history record resource class."""

    def delete(self, file_id):
        """
        Method for HTTP DELETE method working out. Used for deleting history resources.
        Returns:
            Deleted history records in accordance to DELETE method arguments and
            query status.
        """
        history_objects = History.query.filter_by(file_id=file_id).all()
        if history_objects:
            filters_id = list(map(lambda history_object: history_object.filter_id, history_objects))
            for history_object in history_objects:
                delete_from_db(history_object)
            for filter_id in filters_id:
                history_object = History.query.filter_by(filter_id=filter_id).first()
                if not history_object:
                    requests.delete(f'http://127.0.0.1:5000/filter/{filter_id}')
            history = list(map(dump_history_object, history_objects))
            return make_response(jsonify(history), status.HTTP_200_OK)
        return status.HTTP_400_BAD_REQUEST


API.add_resource(HistoryResource, '/history')
API.add_resource(DeleteHistoryRecordResource, '/history/<int:file_id>')
API.add_resource(HistoryRecordResource, '/history/<int:user_id>/<int:file_id>/<int:filter_id>')
