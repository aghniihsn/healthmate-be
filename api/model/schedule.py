from datetime import datetime

from api.index import db

class Schedule(db.Model):
    id_schedule = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    token = db.Column(db.String(250), nullable=False)
    message = db.Column(db.String(250), nullable=False)
    target = db.Column(db.String(20), nullable=False)
    schedule_time = db.Column(db.Time, default=datetime.utcnow)
    schedule_end_date = db.Column(db.Date, nullable=False)
    user_id = db.Column(db.BigInteger, db.ForeignKey('user.user_id', ondelete='CASCADE'))

    def __repr__(self):
        return '<Schedule {}>'.format(self.id_schedule)
