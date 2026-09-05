from datetime import datetime
from app.extensions import db

class Payment(db.Model):
    __tablename__ = 'payments'
    
    id = db.Column(db.Integer, primary_key=True)
    transaction_id = db.Column(db.String(100), unique=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    purpose = db.Column(db.String(150), default='Logistics Support Grant')
    status = db.Column(db.String(30), default='SUCCESS')  # PENDING, SUCCESS, FAILED, REFUNDED
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        user_info = self.user.to_dict() if self.user else {}
        return {
            'id': self.id,
            'transaction_id': self.transaction_id,
            'user_id': self.user_id,
            'username': user_info.get('username'),
            'amount': self.amount,
            'purpose': self.purpose,
            'status': self.status,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
