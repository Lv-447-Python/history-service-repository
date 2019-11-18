"""Module for history model."""
import datetime
from history_service import db


class History(db.Model):
    """History model class."""
    __tablename__ = 'history'

    file_id = db.Column(db.Integer, primary_key=True)
    filter_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, primary_key=True)
    rows_id = db.Column(db.String, nullable=False)
    filter_date = db.Column(db.DateTime, default=datetime.datetime.now())

    def save(self):
        """
        Method for object saving into database.
        Returns:
            None.
        """
        db.session.add(self)
        db.session.commit()

    def delete(self):
        """
        Method for deleting object from database.
        Returns:
            None.
        """
        db.session.delete(self)
        db.session.commit()
