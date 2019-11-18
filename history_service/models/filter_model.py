"""Module for filter model."""
from history_service import DB


class Filter(DB.Model):
    """Filter model class."""
    __tablename__ = 'filter'

    filter_data = DB.Column(DB.String, unique=True, nullable=False)
    filter_id = DB.Column(DB.Integer, primary_key=True, autoincrement=True)
