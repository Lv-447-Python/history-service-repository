import datetime
from history_service import db
from history_service.models.filter_model import Filter


class History(db.Model):
    __tablename__ = 'history'

    file_id = db.Column(db.Integer, primary_key=True)
    filter_id = db.Column(db.Integer, db.ForeignKey('filter.filter_id'), primary_key=True)
    user_id = db.Column(db.Integer, primary_key=True)
    rows_id = db.Column(db.String, nullable=False)
    filter_date = db.Column(db.DateTime, default=datetime.datetime.now())

    def __repr__(self):
        return f'file-{self.file_id}||filter-{self.filter_id}||user-{self.user_id}||rows-{self.rows_id}||date-{self.filter_date}'

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
