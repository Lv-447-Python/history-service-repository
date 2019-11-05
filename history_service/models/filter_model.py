from history_service import db
from sqlalchemy.dialects.postgresql import JSON
from sqlalchemy.orm import relationship


class Filter(db.Model):
    __tablename__ = 'filter'

    filter_data = db.Column(JSON, nullable=False)
    filter_id = db.Column(db.Integer, primary_key=True)
    history = db.relationship('History', backref='filter_id')

    def __init__(self, filter_data, filter_id):
        self.filter_data = filter_data
        self.filter_id = filter_id

    def __repr__(self):
        return f'filter data{self.filter_data}-filter id{self.filter_id}'
