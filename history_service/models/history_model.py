"""Module for history model."""
import datetime
from history_service import DB


class History(DB.Model):
    """History model class."""
    __tablename__ = 'history'

    file_id = DB.Column(DB.Integer, primary_key=True)
    filter_id = DB.Column(DB.Integer, primary_key=True)
    user_id = DB.Column(DB.Integer, primary_key=True)
    rows_id = DB.Column(DB.String, nullable=False)
    filter_date = DB.Column(DB.DateTime, default=datetime.datetime.utcnow())
