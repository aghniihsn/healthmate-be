from datetime import datetime

from api.index import db

class Reminder(db.Model):
    id_reminder = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    id_medicine = db.Column(db.BigInteger, db.ForeignKey('medicine.id_medicine', ondelete='CASCADE'))
    reminder_time = db.Column(db.Time, nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    description = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.BigInteger, db.ForeignKey('user.user_id', ondelete='CASCADE'))
    
    def __repr__(self):
        return '<Reminder {}>'.format(self.id_reminder)
