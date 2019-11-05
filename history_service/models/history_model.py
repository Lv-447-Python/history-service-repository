import datetime
from history_service import db
from sqlalchemy.dialects.postgresql import JSON



class History(db.Model):
    __tablename__ = 'history'

    file_id = db.Column(db.Integer, primary_key=True)
    filter_id = db.Column(db.Integer, db.ForeignKey('filter.id'), primary_key=True)
    user_id = db.Column(db.Integer, primary_key=True)
    rows_id = db.Column(JSON, nullable=False)
    filter_date = db.Column(db.DateTime, default=datetime.datetime.now())

    def __init__(self, file_id, filter_id, user_id, rows_id):
        self.file_id = file_id
        self.filter_id = filter_id
        self.user_id = user_id
        self.rows_id = rows_id

    def __repr__(self):
        return f'file{self.file_id}-filter{self.file_id}-user{self.user_id}-rows{self.rows_id}-date{self.filter_date}'
