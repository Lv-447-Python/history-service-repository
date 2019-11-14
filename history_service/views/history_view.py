import json
import requests
from flask import request
from flask_restful import Resource
from flask_api import status
from marshmallow.exceptions import ValidationError
from history_service import api
from history_service import app
from history_service.views.filter_view import jsonify_data
from history_service.models.history_model import History
from history_service.serializers.history_serializer import HistorySchema


class HistoryResource(Resource):

    @staticmethod
    def dump_history_object(history_object):
        history_serializer = HistorySchema()
        history = history_serializer.dump(history_object)
        history['rows_id'] = json.loads(history['rows_id'])
        return history

    @staticmethod
    def load_history_object(history):
        history_serializer = HistorySchema()
        history_object = history_serializer.load(history)
        return history_object

    def get(self):
        history_data = {
            'user_id': request.args.get('user_id', type=int),
            'file_id': request.args.get('file_id', type=int),
            'filter_id': request.args.get('filter_id', type=int)
        }
        not_empty_fields = {field: value for field, value in history_data.items() if value}
        history_objects = History.query.filter_by(**not_empty_fields).all()
        if history_objects:
            history = [HistoryResource.dump_history_object(history_object) for history_object in history_objects]
            return jsonify_data(history, '', status.HTTP_200_OK)
        return jsonify_data({}, 'History method get: invalid input data!', status.HTTP_400_BAD_REQUEST)

    def post(self):
        history_record = request.get_json()

        try:
            history = {
                'user_id': history_record['user_id'],
                'file_id': history_record['file_id'],
                'rows_id': json.dumps(history_record['rows_id'])
            }
            filter = {'filter_data': history_record['filter_data']}
        except KeyError as key_error:
            app.logger.exception(key_error)
            return jsonify_data({}, 'History method post: invalid input json!', status.HTTP_400_BAD_REQUEST)

        new_filter = requests.post('http://127.0.0.1:5000/filter', json=filter)
        response = new_filter.json()
        # marshmallow.exceptions.ValidationError: {'filter_id': ['Unknown field.']}
        # history['filter_id'] = response['data']['filter_id']

        try:
            history_object = HistoryResource.load_history_object(history)
        except ValidationError as validation_error:
            app.logger.exception(validation_error)
            return jsonify_data({}, 'History method post: serialization error!', status.HTTP_400_BAD_REQUEST)

        history_object.filter_id = response['data']['filter_id']

        existing_history_record = History.query.filter_by(
            user_id=history_object.user_id,
            file_id=history_object.file_id,
            filter_id=history_object.filter_id).first()

        if not existing_history_record:
            history_object.save()
            new_history = HistoryResource.dump_history_object(history_object)
            return jsonify_data(new_history, '', status.HTTP_200_OK)

        return jsonify_data({}, 'History method post: invalid input data!', status.HTTP_400_BAD_REQUEST)

    def delete(self):
        file_id = request.args.get('file_id', type=int)
        if file_id:
            history_objects = History.query.filter_by(file_id=file_id).all()
            filters_id = [history_object.filter_id for history_object in history_objects]
            for history_object in history_objects:
                history_object.delete()
            for filter_id in filters_id:
                history_object = History.query.filter_by(filter_id=filter_id).first()
                if not history_object:
                    deleted_filter = requests.delete(f'http://127.0.0.1:5000/filter?filter_id={filter_id}')
            history = [HistoryResource.dump_history_object(history_object) for history_object in history_objects]
            return jsonify_data(history, '', status.HTTP_200_OK)
        return jsonify_data({}, 'History method delete: invalid input data!', status.HTTP_400_BAD_REQUEST)


api.add_resource(HistoryResource, '/history')
