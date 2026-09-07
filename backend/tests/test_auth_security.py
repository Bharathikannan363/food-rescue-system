"""Auth failures and cross-user authorization (ownership) guards."""
from tests.helpers import PNG, auth, login, post_food, run_lifecycle, set_status, upload_proof
import io


def test_wrong_captcha_rejected(client):
    r = client.post('/api/auth/login', json={
        'username': 'admin', 'password': 'Admin@123',
        'captcha_id': 'does-not-exist', 'captcha_code': 'AAAAA'})
    assert r.status_code == 400


def test_wrong_password_rejected(client):
    r = client.get('/api/auth/captcha')
    captcha = r.get_json()
    r = client.post('/api/auth/login', json={
        'username': 'admin', 'password': 'nope', 'captcha_id': captcha['captcha_id'],
        'captcha_code': captcha['code']})
    assert r.status_code == 401


def test_ngo_token_blocked_from_admin_endpoints(client, tokens):
    r = client.get('/api/admin/assignments', headers=auth(tokens('ngo')))
    assert r.status_code == 403


def test_wrong_volunteer_cannot_respond_update_or_upload(client, tokens, ids):
    """Assignment owned by volunteer1: volunteer2 must get 403 on all three
    volunteer write endpoints."""
    donor, ngo, admin, vol1 = (tokens('donor'), tokens('ngo'),
                               tokens('admin'), tokens('volunteer'))
    vol2 = tokens('volunteer2')
    _, body = post_food(client, donor, title='Own-Guard Food')
    flow = run_lifecycle(client, donor, ngo, admin, vol1, body['donation']['id'])
    aid = flow['assignment_id']

    # ASSIGNED state: volunteer2 cannot respond or update
    r = client.post(f'/api/volunteer/assignments/{aid}/respond',
                    json={'action': 'ACCEPT'}, headers=auth(vol2))
    assert r.status_code == 403
    st, _ = set_status(client, vol2, aid, 'PICKED_UP')
    assert st == 403

    # Move to transit as the owner, then volunteer2 cannot upload proof
    assert set_status(client, vol1, aid, 'PICKED_UP')[0] == 200
    assert set_status(client, vol1, aid, 'OUT_FOR_DELIVERY')[0] == 200
    st, _ = upload_proof(client, vol2, aid)
    assert st == 403


def test_wrong_ngo_cannot_confirm_or_see_location(client, tokens, ids):
    donor, ngo1, ngo2, admin, vol1 = (tokens('donor'), tokens('ngo'), tokens('ngo2'),
                                      tokens('admin'), tokens('volunteer'))
    _, body = post_food(client, donor, title='NGO-Guard Food')
    flow = run_lifecycle(client, donor, ngo1, admin, vol1, body['donation']['id'])
    aid = flow['assignment_id']
    request_id = flow['request_id']

    r = client.post('/api/ngo/confirm-delivery',
                    json={'delivery_id': aid, 'beneficiary_count': 5}, headers=auth(ngo2))
    assert r.status_code == 403

    r = client.get(f'/api/ngo/assignments/{request_id}/location', headers=auth(ngo2))
    assert r.status_code == 403


def test_proof_upload_syncs_assignment_and_donation(client, tokens, ids):
    """Regression: proof upload must move assignment AND donation to DELIVERED."""
    donor, ngo1, admin, vol1 = (tokens('donor'), tokens('ngo'), tokens('admin'),
                                tokens('volunteer'))
    _, body = post_food(client, donor, title='Proof-Sync Food')
    donation_id = body['donation']['id']
    flow = run_lifecycle(client, donor, ngo1, admin, vol1, donation_id)
    aid = flow['assignment_id']

    client.post(f'/api/volunteer/assignments/{aid}/respond', json={'action': 'ACCEPT'},
                headers=auth(vol1))
    set_status(client, vol1, aid, 'PICKED_UP')
    set_status(client, vol1, aid, 'OUT_FOR_DELIVERY')

    st, body = upload_proof(client, vol1, aid)
    assert st == 200

    r = client.get('/api/volunteer/assignments', headers=auth(vol1))
    assignment = [a for a in r.get_json()['assignments'] if a['id'] == aid][0]
    assert assignment['status'] == 'DELIVERED'

    r = client.get('/api/admin/donations', headers=auth(admin))
    donation = [d for d in r.get_json()['donations'] if d['id'] == donation_id][0]
    assert donation['status'] == 'DELIVERED'
