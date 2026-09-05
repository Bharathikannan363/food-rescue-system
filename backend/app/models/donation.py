from datetime import datetime
from app.extensions import db

class Donation(db.Model):
    __tablename__ = 'donations'
    
    id = db.Column(db.Integer, primary_key=True)
    donor_id = db.Column(db.Integer, db.ForeignKey('donors.id'), nullable=False)
    title = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text, nullable=True)
    food_type = db.Column(db.String(50), nullable=False)  # Cooked Meals, Raw Groceries, Bakery Items, Fruits & Veggies, Packaged Goods
    quantity = db.Column(db.String(50), nullable=False)  # e.g., "50 kg", "20 Meals"
    image = db.Column(db.String(255), nullable=True)
    pickup_address = db.Column(db.String(255), nullable=False)
    latitude = db.Column(db.Float, nullable=True)
    longitude = db.Column(db.Float, nullable=True)
    allowed_ngo_id = db.Column(db.Integer, db.ForeignKey('ngos.id'), nullable=True)  # Optional specific NGO permission
    status = db.Column(db.String(30), default='PENDING_ADMIN_APPROVAL')
    # PENDING_ADMIN_APPROVAL, APPROVED, NGO_REQUESTED, DONOR_ACCEPTED, VOLUNTEER_ASSIGNED, PICKED_UP, OUT_FOR_DELIVERY, DELIVERED, COMPLETED, REJECTED, CANCELLED, EXPIRED
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    cancelled_at = db.Column(db.DateTime, nullable=True)

    requests = db.relationship('Request', backref='donation', lazy=True, cascade="all, delete-orphan")

    def to_dict(self):
        donor_info = self.donor.to_dict() if self.donor else {}
        return {
            'id': self.id,
            'donor_id': self.donor_id,
            'donor_name': donor_info.get('organization_name') or donor_info.get('username') or 'Donor',
            'donor_phone': donor_info.get('phone'),
            'title': self.title,
            'description': self.description,
            'food_type': self.food_type,
            'quantity': self.quantity,
            'image': self.image,
            'pickup_address': self.pickup_address,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'allowed_ngo_id': self.allowed_ngo_id,
            'status': self.status,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'cancelled_at': self.cancelled_at.isoformat() if self.cancelled_at else None
        }
