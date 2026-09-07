"""Expiry validation: state computation, input validation, and server-side blocks."""
from tests.helpers import auth, post_food


def test_seeded_expiry_states_computed(client, tokens):
    token = tokens('donor')
    r = client.get('/api/donor/my-donations', headers=auth(token))
    states = {d['title']: d['expiry_state'] for d in r.get_json()['donations']}
    assert states['Seed Fresh'] == 'FRESH'
    assert states['Seed Expiring Soon'] == 'EXPIRING_SOON'
    assert states['Seed Expired'] == 'EXPIRED'


def test_new_donation_expiry_states_persist(client, tokens):
    token = tokens('donor')
    st, body = post_food(client, token, title='Soon Food', expiry_minutes=60)
    assert st == 201 and body['donation']['expiry_state'] == 'EXPIRING_SOON'
    assert body['donation']['expiry_time'] is not None

    st, body = post_food(client, token, title='Far Food', expiry_minutes=600)
    assert st == 201 and body['donation']['expiry_state'] == 'FRESH'

    st, body = post_food(client, token, title='No Expiry Food', expiry_minutes=None)
    assert st == 201 and body['donation']['expiry_state'] == 'NO_EXPIRY_INFO'


def test_invalid_expiry_inputs_rejected(client, tokens):
    token = tokens('donor')
    st, body = post_food(client, token, title='Bad Expiry', expiry_minutes=-30,
                         prep_minutes=-90)
    assert st == 400 and 'future' in body['message']

    st, body = post_food(client, token, title='Prep After Expiry',
                         expiry_minutes=60, prep_minutes=90)
    assert st == 400 and 'after the preparation' in body['message']

    # Malformed string
    r = client.post('/api/donor/post-food',
                    data={'title': 'X', 'quantity': '1', 'pickup_address': 'Y',
                          'expiry_time': 'not-a-date'},
                    headers=auth(token), content_type='multipart/form-data')
    assert r.status_code == 400 and 'Invalid expiry' in r.get_json()['message']


def test_expired_donation_cannot_be_requested(client, tokens):
    ngo = tokens('ngo')
    r = client.get('/api/ngo/available-donations', headers=auth(ngo))
    expired = [d for d in r.get_json()['donations'] if d['title'] == 'Seed Expired']
    assert expired, 'expired donation should still be visible (flagged, not hidden)'
    assert expired[0]['expiry_state'] == 'EXPIRED'

    r = client.post('/api/ngo/request-food',
                    json={'donation_id': expired[0]['id'], 'quality_status': 'VERIFIED'},
                    headers=auth(ngo))
    assert r.status_code == 400
    assert 'expired' in r.get_json()['message'].lower()
