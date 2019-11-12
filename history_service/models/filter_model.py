from history_service import db



class Filter(db.Model):
    __tablename__ = 'filter'

    filter_data = db.Column(db.String, unique=True, nullable=False)
    filter_id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    def __repr__(self):
        return f'filter_id-{self.filter_id}||filter_data-{self.filter_data}'

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
