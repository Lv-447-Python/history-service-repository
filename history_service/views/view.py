from history_service import db
from history_service import api
from history_service.models.history_model import History
from history_service.models.filter_model import Filter
from history_service.serializers.filter_serializer import FilterSchema
from flask import jsonify
from flask_restful import Resource


class FilterResource(Resource):
    def get(self):
        return 'Hello world!'


class HistoryResource(Resource):

    def get(self, file_id, filter_id, user_id):
        return 'Hello world!'


api.add_resource(HistoryResource, '/<int:file_id>/<int:filter_id>/<int:user_id>')
api.add_resource(FilterResource, '/filter')

