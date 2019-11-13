import json
from flask import jsonify, request
from flask_restful import Resource
from flask_api import status
from marshmallow.exceptions import ValidationError
from history_service import api
from history_service import app
from history_service.models.filter_model import Filter
from history_service.serializers.filter_serializer import FilterSchema


def jsonify_data(data, errors, status_code):
    return jsonify({
        'data': data,
        'errors': errors,
        'status': status_code
    })


class FilterResource(Resource):

    @staticmethod
    def dump_filter_object(filter_object):
        filter_serializer = FilterSchema()
        filter = filter_serializer.dump(filter_object)
        filter['filter_data'] = json.loads(filter['filter_data'])
        return filter

    def get(self):
        filter_id = request.args.get('filter_id', type=int)
        if filter_id:
            filter_object = Filter.query.filter_by(filter_id=filter_id).first()
            if filter_object:
                filter = FilterResource.dump_filter_object(filter_object)
                return jsonify_data(filter, '', status.HTTP_200_OK)
        return jsonify_data({}, 'Filter method get: invalid input data!', status.HTTP_400_BAD_REQUEST)

    def post(self):
        filter = request.get_json()
        try:
            filter['filter_data'] = json.dumps(filter['filter_data'])
        except KeyError as key_error:
            app.logger.exception(key_error)
            return jsonify_data({}, 'Filter method post: invalid input json!', status.HTTP_400_BAD_REQUEST)

        filter_serializer = FilterSchema()
        try:
            filter_object = filter_serializer.load(filter)
        except ValidationError as validation_error:
            app.logger.exception(validation_error)
            return jsonify_data({}, 'Filter method post: serialization error!', status.HTTP_400_BAD_REQUEST)
        existing_filter = Filter.query.filter_by(filter_data=filter_object.filter_data).first()

        if not existing_filter:
            filter_object.save()
            new_filter = FilterResource.dump_filter_object(filter_object)
            return jsonify_data(new_filter, '', status.HTTP_200_OK)
        new_filter = FilterResource.dump_filter_object(existing_filter)
        return jsonify_data(new_filter, '', status.HTTP_200_OK)

    def delete(self):
        filter_id = request.args.get('filter_id', type=int)
        if filter_id:
            filter_object = Filter.query.filter_by(filter_id=filter_id).first()
            if filter_object:
                filter_object.delete()
                filter = FilterResource.dump_filter_object(filter_object)
                return jsonify_data(filter, '', status.HTTP_200_OK)
        return jsonify_data({}, 'Filter method delete: invalid input data!', status.HTTP_400_BAD_REQUEST)


api.add_resource(FilterResource, '/filter')
