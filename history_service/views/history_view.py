"""Module for history resource."""
import json
import requests
from flask import request, jsonify, make_response
from flask_restful import Resource
from flask_api import status
from marshmallow.exceptions import ValidationError
from history_service import API
from history_service.models.history_model import History
from history_service.models.filter_model import Filter
from history_service.utils.utils import save_into_db, delete_from_db
from history_service.utils.utils import dump_filter_object, dump_history_object
from history_service.utils.utils import load_filter_object, load_history_object


class HistoryResource(Resource):
    """History resource class."""

    @staticmethod
    def create_new_filter(filter_object):
        existing_filter = Filter.query.filter_by(filter_data=filter_object.filter_data).first()
        if not existing_filter:
            save_into_db(filter_object)
            return filter_object
        return existing_filter

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
            history_value = {
                'user_id': history_record['user_id'],
                'file_id': history_record['file_id'],
                'rows_id': json.dumps(history_record['rows_id'])
            }
            filter_value = {'filter_data': json.dumps(history_record['filter_data'])}
        except KeyError:
            return make_response({}, status.HTTP_400_BAD_REQUEST)

        try:
            filter_object = load_filter_object(filter_value)
        except ValidationError:
            return make_response({}, status.HTTP_400_BAD_REQUEST)

        filter_object = HistoryResource.create_new_filter(filter_object)
        history_value['filter_id'] = filter_object.filter_id

        try:
            history_object = load_history_object(history_value)
        except ValidationError:
            return make_response({}, status.HTTP_400_BAD_REQUEST)

        existing_history_record = History.query.filter_by(
            user_id=history_object.user_id,
            file_id=history_object.file_id,
            filter_id=history_object.filter_id).first()

        if not existing_history_record:
            save_into_db(history_object)
            new_history = dump_history_object(history_object)
            return make_response(jsonify(new_history), status.HTTP_201_CREATED)

        return make_response({}, status.HTTP_400_BAD_REQUEST)


class HistoryRecordResource(Resource):
    """History record resource class."""

    def get(self, user_id, file_id, filter_id):
        """
        Method for HTTP GET method working out. Used for getting history resources.
        Returns:
            History records in accordance to GET method arguments and query status.
        """
        history_data = {
            'user_id': user_id,
            'file_id': file_id,
            'filter_id': filter_id
        }
        history_object = History.query.filter_by(**history_data).first()
        if history_object:
            history_record = dump_history_object(history_object)
            return make_response(jsonify(history_record), status.HTTP_200_OK)
        return make_response({}, status.HTTP_400_BAD_REQUEST)


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
                    filter_object = Filter.query.filter_by(filter_id=filter_id).first()
                    delete_from_db(filter_object)

            history = list(map(dump_history_object, history_objects))
            return make_response(jsonify(history), status.HTTP_200_OK)
        return make_response({}, status.HTTP_400_BAD_REQUEST)


API.add_resource(HistoryResource, '/history')
API.add_resource(DeleteHistoryRecordResource, '/history/<int:file_id>')
API.add_resource(HistoryRecordResource, '/history/<int:user_id>/<int:file_id>/<int:filter_id>')
