"""Shared HTTP helpers for the API tests."""
import io
from datetime import datetime, timedelta, timezone

# 1x1 transparent PNG
PNG = bytes.fromhex(
    '89504e470d0a1a0a0000000d49484452000000010000000108060000001f15c489'
    '0000000d49444154789c626001000000ffff03000006000557bfabd400000000'
    '49454e44ae426082'
)


def auth(token):
    return {'Authorization': f'Bearer {token}'}


def login(client, username, password):
    r = client.get('/api/auth/captcha')
    captcha = r.get_json()
    r = client.post('/api/auth/login', json={
        'username': username, 'password': password,
        'captcha_id': captcha['captcha_id'], 'captcha_code': captcha['code'],
    })
    assert r.status_code == 200, r.get_json()
    return r.get_json()['token']


def post_food(client, token, title='Test Food', expiry_minutes=None,
              prep_minutes=-30, lat=28.6139, lng=77.2090):
    """POST /donor/post-food as multipart. Returns (status, body)."""
    now = datetime.now(timezone.utc)
    data = {
        'title': title, 'food_type': 'Cooked Meals', 'quantity': '5 Plates',
        'description': 'test batch', 'pickup_address': '1 Pickup Street',
        'latitude': str(lat), 'longitude': str(lng),
        'image': (io.BytesIO(PNG), 'f.png', 'image/png'),
    }
    if expiry_minutes is not None:
        data['expiry_time'] = (now + timedelta(minutes=expiry_minutes)).isoformat()
    if prep_minutes is not None:
        data['prep_time'] = (now + timedelta(minutes=prep_minutes)).isoformat()
    r = client.post('/api/donor/post-food', data=data, headers=auth(token),
                    content_type='multipart/form-data')
    return r.status_code, r.get_json()


def run_lifecycle(client, donor, ngo, admin, vol, donation_id):
    """Drive request -> accept -> assign -> deliver -> confirm. Returns dict of ids."""
    r = client.post('/api/ngo/request-food', json={'donation_id': donation_id,
                     'quality_status': 'VERIFIED', 'quality_notes': 'ok'}, headers=auth(ngo))
    assert r.status_code == 200, r.get_json()
    request_id = r.get_json()['request']['id']

    r = client.post(f'/api/donor/requests/{request_id}/respond',
                    json={'action': 'ACCEPT'}, headers=auth(donor))
    assert r.status_code == 200, r.get_json()

    r = client.post('/api/admin/assign-volunteer',
                    json={'request_id': request_id, 'volunteer_id': 1}, headers=auth(admin))
    assert r.status_code == 200, r.get_json()
    assignment_id = r.get_json()['assignment']['id']
    assign_distance = r.get_json().get('distance_km')

    r = client.post(f'/api/volunteer/assignments/{assignment_id}/respond',
                    json={'action': 'ACCEPT'}, headers=auth(vol))
    assert r.status_code == 200, r.get_json()
    return {'request_id': request_id, 'assignment_id': assignment_id,
            'assign_distance': assign_distance}


def set_status(client, vol, assignment_id, status):
    r = client.post('/api/volunteer/update-status',
                    json={'assignment_id': assignment_id, 'status': status}, headers=auth(vol))
    return r.status_code, r.get_json()


def upload_proof(client, token, assignment_id):
    r = client.post('/api/volunteer/upload-proof',
                    data={'assignment_id': str(assignment_id),
                          'proof_image': (io.BytesIO(PNG), 'p.png', 'image/png')},
                    headers=auth(token), content_type='multipart/form-data')
    return r.status_code, r.get_json()
