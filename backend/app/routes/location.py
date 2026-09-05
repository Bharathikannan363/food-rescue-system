from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required
from app.models.volunteer import Volunteer
from app.models.location import VolunteerLocation

location_bp = Blueprint('location', __name__, url_prefix='/api/location')

@location_bp.route('/volunteers', methods=['GET'])
@jwt_required()
def get_all_locations():
    volunteers = Volunteer.query.all()
    results = []
    for v in volunteers:
        latest = VolunteerLocation.query.filter_by(volunteer_id=v.id).order_by(VolunteerLocation.timestamp.desc()).first()
        results.append({
            'volunteer_id': v.id,
            'full_name': v.full_name,
            'latitude': latest.latitude if latest else v.latitude,
            'longitude': latest.longitude if latest else v.longitude,
            'vehicle_type': v.vehicle_type,
            'timestamp': latest.timestamp.isoformat() if latest else None
        })
    return jsonify({'success': True, 'volunteers': results})
