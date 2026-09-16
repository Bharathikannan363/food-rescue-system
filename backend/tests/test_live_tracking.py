"""Tests for live location tracking endpoints."""
from tests.helpers import login, auth

def test_live_feed_accessible_to_all_roles(client):
    admin_token = login(client, 'admin', 'Admin@123')
    ngo_token = login(client, 'ngo', 'Ngo@123')
    donor_token = login(client, 'donor', 'Donor@123')
    vol_token = login(client, 'volunteer', 'Volunteer@123')

    for role_name, token in [('ADMIN', admin_token), ('NGO', ngo_token), ('DONOR', donor_token), ('VOLUNTEER', vol_token)]:
        r = client.get('/api/location/live-feed', headers=auth(token))
        assert r.status_code == 200, f"Role {role_name} failed: {r.get_json()}"
        data = r.get_json()
        assert data['success'] is True
        assert 'current_user' in data
        assert data['current_user']['role'] == role_name
        assert 'volunteers' in data
        assert 'donors' in data
        assert 'ngos' in data
        assert 'active_deliveries' in data

def test_volunteer_location_update(client):
    vol_token = login(client, 'volunteer', 'Volunteer@123')
    orig_lat, orig_lng = 28.6200, 77.2140
    new_lat = 28.6190
    new_lng = 28.6135

    r = client.post('/api/location/update', json={
        'latitude': new_lat,
        'longitude': new_lng
    }, headers=auth(vol_token))

    assert r.status_code == 200
    data = r.get_json()
    assert data['success'] is True
    assert data['latitude'] == new_lat
    assert data['longitude'] == new_lng

    # Verify updated coordinates reflected in live feed
    r2 = client.get('/api/location/live-feed', headers=auth(vol_token))
    assert r2.status_code == 200
    feed = r2.get_json()
    assert feed['current_user']['latitude'] == new_lat
    assert feed['current_user']['longitude'] == new_lng

    # Restore original position so order in test_proximity is preserved
    client.post('/api/location/update', json={
        'latitude': orig_lat,
        'longitude': orig_lng
    }, headers=auth(vol_token))

def test_volunteers_list_endpoint(client):
    donor_token = login(client, 'donor', 'Donor@123')
    r = client.get('/api/location/volunteers', headers=auth(donor_token))
    assert r.status_code == 200
    data = r.get_json()
    assert data['success'] is True
    assert isinstance(data['volunteers'], list)
    assert len(data['volunteers']) > 0
    first_vol = data['volunteers'][0]
    assert 'full_name' in first_vol
    assert 'latitude' in first_vol
    assert 'longitude' in first_vol
