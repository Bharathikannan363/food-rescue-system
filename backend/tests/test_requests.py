"""NGO request rules: duplicate blocking and re-request after donor rejection."""
from tests.helpers import auth, post_food


def test_duplicate_active_request_blocked_then_allowed_after_rejection(client, tokens):
    donor, ngo = tokens('donor'), tokens('ngo')
    _, body = post_food(client, donor, title='Dedup Food')
    donation_id = body['donation']['id']

    r = client.post('/api/ngo/request-food',
                    json={'donation_id': donation_id, 'quality_status': 'VERIFIED'},
                    headers=auth(ngo))
    assert r.status_code == 200
    request_id = r.get_json()['request']['id']

    # Same NGO, same donation while request is PENDING -> blocked
    r = client.post('/api/ngo/request-food',
                    json={'donation_id': donation_id, 'quality_status': 'VERIFIED'},
                    headers=auth(ngo))
    assert r.status_code == 400
    assert 'already submitted' in r.get_json()['message']

    # Donor rejects -> donation re-opens; the SAME NGO must be able to re-request
    r = client.post(f'/api/donor/requests/{request_id}/respond',
                    json={'action': 'REJECT'}, headers=auth(donor))
    assert r.status_code == 200

    r = client.post('/api/ngo/request-food',
                    json={'donation_id': donation_id, 'quality_status': 'VERIFIED'},
                    headers=auth(ngo))
    assert r.status_code == 200, r.get_json()


def test_cancelled_donation_hidden_from_ngo_browse(client, tokens):
    donor, ngo = tokens('donor'), tokens('ngo')
    _, body = post_food(client, donor, title='Cancel-Hide Food')

    r = client.post(f"/api/donor/donations/{body['donation']['id']}/cancel",
                    headers=auth(donor))
    assert r.status_code == 200

    r = client.get('/api/ngo/available-donations', headers=auth(ngo))
    titles = [d['title'] for d in r.get_json()['donations']]
    assert 'Cancel-Hide Food' not in titles
