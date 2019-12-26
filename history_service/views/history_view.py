"""Module for history resource."""
import json
import requests
from flask import request, jsonify, make_response
from flask_restful import Resource
from flask_api import status
from marshmallow.exceptions import ValidationError
from history_service import API
from history_service.configs.logger import LOGGER
from history_service.models.history_model import History
from history_service.models.filter_model import Filter
from history_service.utils.utils import save_into_db, delete_from_db
from history_service.utils.utils import dump_history_object, create_error_dictionary
from history_service.utils.utils import load_filter_object, load_history_object
from history_service.utils.utils import get_user_id_by_session


class HistoryResource(Resource):
    """History resource class."""

    @staticmethod
    def create_new_filter(filter_object):
        """
        Add filter object to filter table in database.
        Args:
            filter_object:
                Any instance of Filter model class.
        Returns:
            Updated filter object with id.
        """
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
        LOGGER.info('Successful request to HistoryResource')
        return make_response(jsonify(history), status.HTTP_200_OK)

    def post(self):
        """
        Method for HTTP POST method working out. Used for creation history resources.
        Returns:
            New history records in accordance to request and query status.
        """
        history_record = request.get_json()

        try:
            session = request.cookies['session']
        except KeyError:
            LOGGER.error('There is not any session in headers')
            response_object = create_error_dictionary('There is not session any in headers')
            return make_response(jsonify(response_object), status.HTTP_403_FORBIDDEN)

        user_id = get_user_id_by_session(session)

        try:
            history_value = {
                'user_id': user_id,
                'file_id': history_record['file_id'],
                'rows_id': json.dumps(history_record['rows_id'])
            }
            filter_value = {'filter_data': json.dumps(history_record['filter_data'])}
        except KeyError as key_error:
            LOGGER.error('Key error, %s', key_error)
            response_object = create_error_dictionary(f'Key error, {key_error}')
            return make_response(jsonify(response_object), status.HTTP_400_BAD_REQUEST)

        try:
            filter_object = load_filter_object(filter_value)
        except ValidationError as validation_error:
            LOGGER.error('Validation error, %s', validation_error)
            response_object = create_error_dictionary(f'Validation error, {validation_error}')
            return make_response(jsonify(response_object), status.HTTP_400_BAD_REQUEST)

        filter_object = HistoryResource.create_new_filter(filter_object)
        history_value['filter_id'] = filter_object.filter_id

        try:
            history_object = load_history_object(history_value)
        except ValidationError as validation_error:
            LOGGER.error('Validation error, %s', validation_error)
            response_object = create_error_dictionary(f'Validation error, {validation_error}')
            return make_response(jsonify(response_object), status.HTTP_400_BAD_REQUEST)

        existing_history_record = History.query.filter_by(
            user_id=history_object.user_id,
            file_id=history_object.file_id,
            filter_id=history_object.filter_id).first()

        if not existing_history_record:
            save_into_db(history_object)
            new_history = dump_history_object(history_object)
            LOGGER.info('Successful request to HistoryResource')
            return make_response(jsonify(new_history), status.HTTP_201_CREATED)

        LOGGER.info('This object already exists')
        response_object = create_error_dictionary('This object already exists.')
        return make_response(jsonify(response_object), status.HTTP_201_CREATED)


class HistoryRecordResource(Resource):
    """History record resource class."""

    def get(self, file_id, filter_id):
        """
        Method for HTTP GET method working out. Used for getting history resources.
        Args:
            file_id:
                File identifier.
            filter_id:
                Filter identifier.
        Returns:
            History records in accordance to GET method arguments and query status.
        """

        try:
            session = request.cookies['session']
        except KeyError:
            LOGGER.error('There is not any session in headers')
            response_object = create_error_dictionary('There is not session any in headers')
            return make_response(jsonify(response_object), status.HTTP_403_FORBIDDEN)

        user_id = get_user_id_by_session(session)

        history_data = {
            'user_id': user_id,
            'file_id': file_id,
            'filter_id': filter_id
        }
        history_object = History.query.filter_by(**history_data).first()
        if history_object:
            history_record = dump_history_object(history_object)
            LOGGER.info('Successful request to HistoryRecordResource')
            return make_response(jsonify(history_record), status.HTTP_200_OK)
        LOGGER.error('There isn\'t data with this parameters')
        response_object = create_error_dictionary('There isn\'t data with this parameters')
        return make_response(jsonify(response_object), status.HTTP_400_BAD_REQUEST)


class UserHistoryResource(Resource):
    """User history resource class."""

    def get(self):
        """
        Method for HTTP GET method working out. Used for getting history resources.
        Returns:
            History records in accordance to GET method arguments and query status.
        """
        try:
            session = request.cookies['session']
        except KeyError:
            LOGGER.error('There is not any session in headers')
            response_object = create_error_dictionary('There is not session any in headers')
            return make_response(jsonify(response_object), status.HTTP_403_FORBIDDEN)

        user_id = get_user_id_by_session(session)
        LOGGER.info("USER_ID %s", user_id)

        history_objects = History.query.filter_by(user_id=user_id).all()
        history = []
        for history_object in history_objects:
            response = requests.get(f'http://web-file:5000/file/{history_object.file_id}')
            if response.status_code != 200:
                LOGGER.error('File service request error')
                response_object = create_error_dictionary('File service request error')
                return make_response(jsonify(response_object),
                                     status.HTTP_500_INTERNAL_SERVER_ERROR)
            response_json = response.json()
            history_record = dump_history_object(history_object)
            try:
                history_record['path'] = response_json['path']
                filter_record = Filter.query.filter_by(filter_id=history_record['filter_id']).first()
            except KeyError as key_error:
                LOGGER.error('File service response error, %s', key_error)
                response_object = create_error_dictionary(f'File service response error, {key_error}')
                return make_response(jsonify(response_object),
                                     status.HTTP_500_INTERNAL_SERVER_ERROR)

            history_record['filter'] = filter_record.filter_data
            history.append(history_record)
        LOGGER.info('Successful request to UserHistoryResource')
        return make_response(jsonify(history), status.HTTP_200_OK)


class FileHistoryResource(Resource):
    """Deleting history record resource class in case of deleting files."""

    def delete(self, file_id):
        """
        Method for HTTP DELETE method working out. Used for deleting history resources.
        Args:
            file_id:
                File identifier.
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
            LOGGER.info('Successful request to FileHistoryResource')
            return make_response(jsonify(history), status.HTTP_200_OK)
        LOGGER.error('There isn\'t data with this parameters')
        response_object = create_error_dictionary('There isn\'t data with this parameters')
        return make_response(jsonify(response_object), status.HTTP_400_BAD_REQUEST)


API.add_resource(HistoryResource, '/history')
API.add_resource(UserHistoryResource, '/history/user')
API.add_resource(FileHistoryResource, '/history/file/<int:file_id>')
API.add_resource(HistoryRecordResource, '/history/file/<int:file_id>'
                                        '/filter/<int:filter_id>')
