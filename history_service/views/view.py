from history_service import db
from history_service import api
from history_service.models.history_model import History
from history_service.models.filter_model import Filter
from history_service.serializers.filter_serializer import FilterSchema
from flask import jsonify, request
from flask_restful import Resource
from flask_api import status
from sqlalchemy import cast
import json


class FilterResource(Resource):

    def get(self):
        filter_id = request.args.get('filter', type=int)
        if filter_id:
            filter_data = Filter.query.filter_by(filter_id=filter_id).first_or_404()
            filter_serializer = FilterSchema()
            return jsonify({'filter': filter_serializer.dump(filter_data)})
        else:
            return status.HTTP_400_BAD_REQUEST

    def post(self):
        filter_data = request.get_json()
        if filter_data:
            if {'user_id', 'file_id', 'filter', 'rows_id'} == set(filter_data.keys()):
                filter_serializer = FilterSchema()
                loaded_filter = filter_serializer.load(filter_data['filter'])
                print(Filter.filter_data['filter_data'].astext)
                print(json.dumps(loaded_filter))
                # https://docs.sqlalchemy.org/en/13/dialects/postgresql.html#sqlalchemy.dialects.postgresql.JSON.Comparator.astext
                if not Filter.query.filter(Filter.filter_data['filter_data'].astext == json.dumps(loaded_filter['filter_data'])).first():
                    new_filter = Filter(loaded_filter)
                    db.session.add(new_filter)
                    db.session.commit()
                else:
                    print('EEEEEEEEEEEEXISTS')
                return status.HTTP_201_CREATED
        return status.HTTP_400_BAD_REQUEST


class HistoryResource(Resource):

    def get(self, file_id, filter_id, user_id):
        return 'Hello world'


api.add_resource(HistoryResource, '/history')
api.add_resource(FilterResource, '/filter')

