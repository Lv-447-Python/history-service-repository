import json
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


class HistoryResource(Resource):

    @staticmethod
    def get_filter_by_history_record(history_record):
        filter_id = history_record.pop('filter_id')
        filter_data = Filter.query.filter_by(filter_id=filter_id).first_or_404()
        filter_serializer = FilterSchema()
        history_record.update({'filter': filter_serializer.dump(filter_data)})

    @staticmethod
    def create_filter_and_return_id(filter_data):
        filter_str = json.dumps(filter_data['filter_data'])
        filter_serializer = FilterSchema()
        loaded_filter = filter_serializer.load({'filter_data': filter_str})
        find_same_filter = Filter.query.filter_by(filter_data=filter_str).first()
        if not find_same_filter:
            db.session.add(loaded_filter)
            db.session.commit()
            new_filter = Filter.query.order_by(Filter.filter_id.desc()).first()
            return new_filter.filter_id
        return find_same_filter.filter_id

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
        history_data = request.get_json()
        if set(history_data.keys()) == {'user_id', 'file_id', 'filter', 'rows_id'}:
            try:
                history_data['filter_id'] = self.create_filter_and_return_id(history_data.pop('filter'))
                history_data['rows_id'] = json.dumps(history_data['rows_id'])
                history_serializer = HistorySchema()
                loaded_history = history_serializer.load(history_data)
                db.session.add(loaded_history)
                db.session.commit()
                return status.HTTP_201_CREATED
            except exc.SQLAlchemyError:
                return status.HTTP_409_CONFLICT
            except InternalServerError:
                return status.HTTP_500_INTERNAL_SERVER_ERROR
        return status.HTTP_400_BAD_REQUEST


api.add_resource(HistoryResource, '/history')
