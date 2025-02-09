from api.index import db
from datetime import datetime

class Notification(db.Model):
    id_notification = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    message = db.Column(db.String(100), nullable=False)
    # is_read = db.Column(db.Boolean, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    id_reminder = db.Column(db.BigInteger, db.ForeignKey('reminder.id_reminder', ondelete='CASCADE'))
    user_id = db.Column(db.BigInteger, db.ForeignKey('user.user_id', ondelete='CASCADE'))

    def __repr__(self):
        return '<Notification {}>'.format(self.id_notification)
