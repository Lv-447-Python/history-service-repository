from history_service import db
from history_service import api
from history_service.models.history_model import History
from flask import jsonify
from flask_restful import Resource


class HistoryResource(Resource):

    def get(self, file_id, filter_id, user_id):
        rows_id = {'rows': [1, 3, 34, 13, 2]}
        history = History(file_id=file_id, filter_id=filter_id, user_id=user_id, rows_id=rows_id)
        db.session.add(history)
        db.session.commit()
        return jsonify({'file_id': file_id, 'filter_id': filter_id, 'user_id': user_id})


api.add_resource(HistoryResource, '/<int:file_id>/<int:filter_id>/<int:user_id>')
