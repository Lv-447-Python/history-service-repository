import json
import requests
from sqlalchemy import exc
from flask import jsonify, request
from flask_restful import Resource
from flask_api import status
from werkzeug.exceptions import InternalServerError
from history_service import db
from history_service import api
from history_service.models.history_model import History
from history_service.models.filter_model import Filter
from history_service.serializers.filter_serializer import FilterSchema
from history_service.serializers.history_serializer import HistorySchema


class FilterResource(Resource):

    def get(self):
        filter_args = request.args
        if set(filter_args.keys()).issubset({'filter_id'}):
            try:
                filter_data = Filter.query.filter_by(**filter_args).first_or_404()
                filter_serializer = FilterSchema()
                return jsonify({'filter': filter_serializer.dump(filter_data)})
            except exc.SQLAlchemyError:
                return status.HTTP_400_BAD_REQUEST
        return status.HTTP_400_BAD_REQUEST

    def post(self):
        post_data_from_history_resources = request.get_json()
        if set(post_data_from_history_resources.keys()) == {'filter'}:
            filter_serializer = FilterSchema()
            loaded_filter = filter_serializer.load(post_data_from_history_resources['filter'])
            # https://docs.sqlalchemy.org/en/13/dialects/postgresql.html#sqlalchemy.dialects.postgresql.JSON.Comparator.astext
            if not Filter.query.filter(Filter.filter_data['filter_data'].astext == json.dumps(loaded_filter['filter_data'])).first():
                new_filter = Filter(loaded_filter['filter_data'])
                db.session.add(new_filter)
                db.session.commit()
            return status.HTTP_201_CREATED
        return status.HTTP_400_BAD_REQUEST


class HistoryResource(Resource):

    @staticmethod
    def get_filter_by_history_record(history_record):
        filter_id = history_record.pop('filter_id')
        filter = requests.get(f'http://localhost:5000/filter?filter_id={filter_id}')
        if filter.status_code == 200:
            history_record.update(filter.json())
        else:
            raise InternalServerError

    def get(self):
        request_args = request.args
        if set(request_args.keys()).issubset({'user_id', 'file_id', 'filter_id'}):
            try:
                history_data = History.query.filter_by(**request_args).all()
                history_serializer = HistorySchema()
                dumped_history = [history_serializer.dump(record) for record in history_data]
                if dumped_history:
                    for record in dumped_history:
                        self.get_filter_by_history_record(record)
                return jsonify({'history': dumped_history})
            except exc.SQLAlchemyError:
                return status.HTTP_400_BAD_REQUEST
        return status.HTTP_400_BAD_REQUEST

    def post(self):
        filter_data = request.get_json()
        if filter_data:
            if set(filter_data.keys()) == {'user_id', 'file_id', 'filter', 'rows_id'}:
                pass
        return status.HTTP_400_BAD_REQUEST


api.add_resource(HistoryResource, '/history')
api.add_resource(FilterResource, '/filter')
