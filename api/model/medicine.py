from datetime import datetime

from api.index import db
class Medicine(db.Model):
    id_medicine = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    medicine_name = db.Column(db.String(250), nullable=False)
    dosage = db.Column(db.String(20), nullable=False)
    frequency = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.BigInteger, db.ForeignKey('user.user_id', ondelete='CASCADE'))

    def __repr__(self):
        return '<Medicine {}>'.format(self.medicine_name)
