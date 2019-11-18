"""Module for history resource."""
import json
import requests
from flask import request
from flask_restful import Resource
from flask_api import status
from marshmallow.exceptions import ValidationError
from history_service import api
from history_service import app
from history_service.utils.utils import jsonify_data
from history_service.models.history_model import History
from history_service.serializers.history_serializer import HistorySchema


class HistoryResource(Resource):
    """History resource class."""

    @staticmethod
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

    @staticmethod
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

    def get(self):
        """
        Method for HTTP GET method working out. Used for getting history resources.
        Returns:
            History records in accordance to GET method arguments, errors and query status.
        """
        history_data = {
            'user_id': request.args.get('user_id', type=int),
            'file_id': request.args.get('file_id', type=int),
            'filter_id': request.args.get('filter_id', type=int)
        }
        not_empty_fields = dict(filter(lambda item: item[1], history_data.items()))
        history_objects = History.query.filter_by(**not_empty_fields).all()
        if history_objects:
            history = list(map(HistoryResource.dump_history_object, history_objects))
            return jsonify_data(history, '', status.HTTP_200_OK)
        return jsonify_data({}, 'History method get: invalid input data!',
                            status.HTTP_400_BAD_REQUEST)

    def post(self):
        """
        Method for HTTP POST method working out. Used for creation history resources.
        Returns:
            New history records in accordance to request, errors and query status.
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
            app.logger.exception(key_error)
            return jsonify_data({}, 'History method post: invalid input json!',
                                status.HTTP_400_BAD_REQUEST)

        new_filter = requests.post('http://127.0.0.1:5000/filter', json=filter_value)
        response = new_filter.json()
        history['filter_id'] = response['data']['filter_id']

        try:
            history_object = HistoryResource.load_history_object(history)
        except ValidationError as validation_error:
            app.logger.exception(validation_error)
            return jsonify_data({}, 'History method post: serialization error!',
                                status.HTTP_400_BAD_REQUEST)

        existing_history_record = History.query.filter_by(
            user_id=history_object.user_id,
            file_id=history_object.file_id,
            filter_id=history_object.filter_id).first()

        if not existing_history_record:
            history_object.save()
            new_history = HistoryResource.dump_history_object(history_object)
            return jsonify_data(new_history, '', status.HTTP_200_OK)

        return jsonify_data({}, 'History method post: invalid input data!',
                            status.HTTP_400_BAD_REQUEST)

    def delete(self):
        """
        Method for HTTP DELETE method working out. Used for deleting history resources.
        Returns:
            Deleted history records in accordance to DELETE method arguments, errors and
            query status.
        """
        file_id = request.args.get('file_id', type=int)
        if file_id:
            history_objects = History.query.filter_by(file_id=file_id).all()
            filters_id = list(map(lambda history_object: history_object.filter_id, history_objects))
            for history_object in history_objects:
                history_object.delete()
            for filter_id in filters_id:
                history_object = History.query.filter_by(filter_id=filter_id).first()
                if not history_object:
                    requests.delete(f'http://127.0.0.1:5000/filter?filter_id={filter_id}')
            history = list(map(HistoryResource.dump_history_object, history_objects))
            return jsonify_data(history, '', status.HTTP_200_OK)
        return jsonify_data({}, 'History method delete: invalid input data!',
                            status.HTTP_400_BAD_REQUEST)


api.add_resource(HistoryResource, '/history')
