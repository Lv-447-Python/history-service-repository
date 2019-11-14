"""Module for filter model."""
from history_service import db


class Filter(db.Model):
    """Filter model class."""
    __tablename__ = 'filter'

    filter_data = db.Column(db.String, unique=True, nullable=False)
    filter_id = db.Column(db.Integer, primary_key=True, autoincrement=True)

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
