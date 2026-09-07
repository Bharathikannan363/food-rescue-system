import os
import sys
from datetime import datetime, timedelta

import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app  # noqa: E402
from app.extensions import db as _db  # noqa: E402
from app.models import (  # noqa: E402
    User, Donor, NGO, Volunteer, Donation, VolunteerLocation
)

# Pickup coordinates shared by seeded donations (donor's registered location)
PICKUP_LAT, PICKUP_LNG = 28.6139, 77.2090

PASSWORDS = {
    'admin': 'Admin@123', 'donor': 'Donor@123',
    'ngo': 'Ngo@123', 'ngo2': 'Ngo2@123',
    'volunteer': 'Volunteer@123', 'volunteer2': 'Volunteer@123',
    'volunteer3': 'Volunteer@123',
}


class TestConfig:
    SECRET_KEY = 'test-secret'
    JWT_SECRET_KEY = 'test-jwt-secret'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024
    TESTING = True


@pytest.fixture(scope='session')
def app(tmp_path_factory):
    TestConfig.SQLALCHEMY_DATABASE_URI = f"sqlite:///{tmp_path_factory.mktemp('db') / 'test.db'}"
    TestConfig.UPLOAD_FOLDER = str(tmp_path_factory.mktemp('uploads'))
    application = create_app(TestConfig)
    yield application


@pytest.fixture(scope='session')
def seeded(app):
    """Create the demo cast once per test session: two NGOs, three volunteers
    (two with GPS pings at different distances, one with no location), and
    donations covering all expiry states."""
    now = datetime.utcnow()
    with app.app_context():
        def make_user(username, role, approved=True):
            u = User(username=username, email=f'{username}@test.org', role=role,
                     phone=f'+91990000{username[-1:] or 0}0', is_approved=approved,
                     approval_status='APPROVED' if approved else 'PENDING')
            u.set_password(PASSWORDS.get(username, 'Pass@123'))
            _db.session.add(u)
            _db.session.flush()
            return u

        make_user('admin', 'ADMIN')
        donor_u = make_user('donor', 'DONOR')
        _db.session.add(Donor(user_id=donor_u.id, organization_name='Test Caterers',
                              address='1 Pickup Street', latitude=PICKUP_LAT, longitude=PICKUP_LNG))

        ngo1 = make_user('ngo', 'NGO')
        _db.session.add(NGO(user_id=ngo1.id, ngo_name='Shelter One', registration_number='R-1',
                            address='2 Shelter Road', latitude=28.6250, longitude=77.2180))
        ngo2 = make_user('ngo2', 'NGO')
        _db.session.add(NGO(user_id=ngo2.id, ngo_name='Shelter Two', registration_number='R-2',
                            address='3 Other Road', latitude=28.7000, longitude=77.3000))

        v1 = make_user('volunteer', 'VOLUNTEER')
        v1p = Volunteer(user_id=v1.id, full_name='Alex Rivera', vehicle_type='Van',
                        is_available=True, latitude=28.6180, longitude=77.2130)
        v2 = make_user('volunteer2', 'VOLUNTEER')
        v2p = Volunteer(user_id=v2.id, full_name='Priya Sharma', vehicle_type='Scooter',
                        is_available=True, latitude=28.6250, longitude=77.2180)
        v3 = make_user('volunteer3', 'VOLUNTEER')
        v3p = Volunteer(user_id=v3.id, full_name='Ravi Kumar', vehicle_type='Bike',
                        is_available=True, latitude=None, longitude=None)
        _db.session.add_all([v1p, v2p, v3p])
        _db.session.flush()

        donor = Donor.query.filter_by(user_id=donor_u.id).first()

        def donation(title, state):
            expiry = {'fresh': now + timedelta(hours=5), 'soon': now + timedelta(minutes=45),
                      'expired': now - timedelta(hours=2)}[state]
            return Donation(donor_id=donor.id, title=title, food_type='Cooked Meals',
                            quantity='10 Plates', pickup_address='1 Pickup Street',
                            latitude=PICKUP_LAT, longitude=PICKUP_LNG,
                            prep_time=now - timedelta(hours=1), expiry_time=expiry,
                            status='APPROVED')

        _db.session.add_all([donation('Seed Fresh', 'fresh'),
                             donation('Seed Expiring Soon', 'soon'),
                             donation('Seed Expired', 'expired')])
        _db.session.add_all([VolunteerLocation(volunteer_id=v1p.id, latitude=28.6200, longitude=77.2140),
                             VolunteerLocation(volunteer_id=v2p.id, latitude=28.6250, longitude=77.2180)])
        _db.session.commit()

        # Expose profile ids for tests without holding model instances across contexts
        app.extensions['test_ids'] = {
            'vol1': v1p.id, 'vol2': v2p.id, 'vol3': v3p.id,
            'ngo1_user': ngo1.id, 'ngo2_user': ngo2.id,
        }
    yield app


@pytest.fixture()
def client(app, seeded):
    return app.test_client()


@pytest.fixture()
def ids(app):
    return app.extensions['test_ids']


@pytest.fixture()
def tokens(client):
    """Lazily log in demo users and cache their JWTs."""
    cache = {}

    def get(username):
        if username not in cache:
            from tests.helpers import login
            cache[username] = login(client, username, PASSWORDS[username])
        return cache[username]
    return get
