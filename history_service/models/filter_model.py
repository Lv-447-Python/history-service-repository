from history_service import db
from sqlalchemy.dialects.postgresql import JSON


class Filter(db.Model):
    __tablename__ = 'filter'

    filter_data = db.Column(JSON, nullable=False, unique=True)
    filter_id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    def __init__(self, filter_data):
        self.filter_data = filter_data

    def __repr__(self):
        return f'filter data{self.filter_data}-filter id{self.filter_id}'
