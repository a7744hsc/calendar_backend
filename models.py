from main import db_alchemy

class Event(db_alchemy.Model):
    __tablename__ = 'events'

    id = db_alchemy.Column(db_alchemy.Integer, primary_key=True)
    event_start = db_alchemy.Column(db_alchemy.DateTime, nullable=False)
    event_end = db_alchemy.Column(db_alchemy.DateTime, nullable=False)
    created_date = db_alchemy.Column(db_alchemy.DateTime, nullable=False)
    last_modified_date = db_alchemy.Column(db_alchemy.DateTime, nullable=False)
    event_owner = db_alchemy.Column(db_alchemy.String(50), nullable=False)
    title = db_alchemy.Column(db_alchemy.String(50), nullable=False)
    details = db_alchemy.Column(db_alchemy.Text(1000))

    def as_dict(self):
       return {c.name: getattr(self, c.name) for c in self.__table__.columns}