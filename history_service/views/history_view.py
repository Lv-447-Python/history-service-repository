import json
import requests
from flask import jsonify, request
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

    def get(self):
        history_data = {
            'user_id': request.args.get('user_id', type=int),
            'file_id': request.args.get('file_id', type=int),
            'filter_id': request.args.get('filter_id', type=int)
        }
        history_objects = History.query.filter_by(**{field: value for field, value in history_data.items() if value}).all()
        if history_objects:
            history = [HistoryResource.dump_history_object(history_object) for history_object in history_objects]
            return jsonify_data(history, '', status.HTTP_200_OK)
        return jsonify_data({}, 'Invalid input data!', status.HTTP_400_BAD_REQUEST)

    def post(self):
        history_record = request.get_json()

        if history_record:
            try:
                history = {
                    'user_id': history_record['user_id'],
                    'file_id': history_record['file_id'],
                    'rows_id': json.dumps(history_record['rows_id'])
                }
                filter = {'filter_data': history_record['filter_data']}
            except KeyError:
                app.logger.exception()
                return jsonify_data({}, 'Invalid input data!', status.HTTP_400_BAD_REQUEST)

            new_filter = requests.post('http://127.0.0.1:5000/filter', json=filter)

            if new_filter.status_code == 200:
                response = new_filter.json()
                # marshmallow.exceptions.ValidationError: {'filter_id': ['Unknown field.']}
                # history['filter_id'] = response['data']
                history_serializer = HistorySchema()
                try:
                    history_object = history_serializer.load(history)
                except ValidationError:
                    app.logger.exception()
                    return status.HTTP_400_BAD_REQUEST
                history_object.filter_id = response['data']['filter_id']
                # primary key unique constraint (key is already existed)
                history_object.save()
                new_history = HistoryResource.dump_history_object(history_object)
                return jsonify_data(new_history, '', status.HTTP_200_OK)

        return jsonify_data({}, 'Invalid input data!', status.HTTP_400_BAD_REQUEST)

    def delete(self):
        pass

    def put(self):
        pass


api.add_resource(HistoryResource, '/history')
