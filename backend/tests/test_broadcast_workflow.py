"""Tests for the Broadcast Workflow:
1. Donor posts food -> Donation Available
2. Multiple NGOs can view -> One NGO accepts -> Status becomes NGO_ACCEPTED -> All volunteers notified
3. Second NGO attempting to accept receives 409 Conflict
4. Multiple volunteers see open tasks -> First volunteer accepts -> Status becomes VOLUNTEER_ASSIGNED
5. Second volunteer attempting to accept receives 409 Conflict
6. Volunteer pickup -> delivery -> NGO confirms beneficiaries
"""
from tests.helpers import auth, post_food, set_status, upload_proof


def test_ngo_view_and_accept_broadcasts_to_volunteers(client, tokens):
    donor = tokens('donor')
    ngo1 = tokens('ngo')
    ngo2 = tokens('ngo2')
    vol1 = tokens('volunteer')

    # 1. Donor posts food
    st, body = post_food(client, donor, title='Broadcast Banquet Meals', expiry_minutes=240)
    assert st == 201
    donation_id = body['donation']['id']

    # 2. Both NGO 1 and NGO 2 can view the available donation
    r1 = client.get('/api/ngo/available-donations', headers=auth(ngo1))
    assert r1.status_code == 200
    avail_ids_ngo1 = [d['id'] for d in r1.get_json()['donations']]
    assert donation_id in avail_ids_ngo1

    r2 = client.get('/api/ngo/available-donations', headers=auth(ngo2))
    assert r2.status_code == 200
    avail_ids_ngo2 = [d['id'] for d in r2.get_json()['donations']]
    assert donation_id in avail_ids_ngo2

    # 3. NGO 1 accepts the donation
    accept_res = client.post('/api/ngo/accept-donation', json={
        'donation_id': donation_id,
        'quality_status': 'VERIFIED',
        'quality_notes': 'Inspected food quality and hygiene.'
    }, headers=auth(ngo1))
    assert accept_res.status_code == 200, accept_res.get_json()
    assert accept_res.get_json()['donation']['status'] == 'NGO_ACCEPTED'

    # 4. NGO 2 attempts to accept the same donation -> gets 409 Conflict
    conflict_res = client.post('/api/ngo/accept-donation', json={
        'donation_id': donation_id,
        'quality_status': 'VERIFIED'
    }, headers=auth(ngo2))
    assert conflict_res.status_code == 409
    assert 'already been accepted by another NGO' in conflict_res.get_json()['message']

    # 5. Volunteers receive notification
    vol_notifs = client.get('/api/notifications', headers=auth(vol1))
    assert vol_notifs.status_code == 200
    notif_titles = [n['title'] for n in vol_notifs.get_json()['notifications']]
    assert any('New Food Delivery Available' in t for t in notif_titles)


def test_volunteer_broadcast_claim_first_come_first_served(client, tokens):
    donor = tokens('donor')
    ngo = tokens('ngo')
    vol1 = tokens('volunteer')
    vol2 = tokens('volunteer2')

    # Donor posts food & NGO accepts
    _, body = post_food(client, donor, title='Claim Test Meals', expiry_minutes=300)
    donation_id = body['donation']['id']

    accept_res = client.post('/api/ngo/accept-donation', json={'donation_id': donation_id}, headers=auth(ngo))
    assert accept_res.status_code == 200
    request_id = accept_res.get_json()['request']['id']

    # Both volunteers query available open tasks
    v1_tasks = client.get('/api/volunteer/available-tasks', headers=auth(vol1)).get_json()['tasks']
    v2_tasks = client.get('/api/volunteer/available-tasks', headers=auth(vol2)).get_json()['tasks']

    assert any(t['request_id'] == request_id for t in v1_tasks)
    assert any(t['request_id'] == request_id for t in v2_tasks)

    # First volunteer (vol1) claims the delivery task
    claim1 = client.post('/api/volunteer/claim-task', json={'request_id': request_id}, headers=auth(vol1))
    assert claim1.status_code == 201, claim1.get_json()
    assign_id = claim1.get_json()['assignment']['id']

    # Second volunteer (vol2) attempts to claim the same delivery task -> receives 409 Conflict
    claim2 = client.post('/api/volunteer/claim-task', json={'request_id': request_id}, headers=auth(vol2))
    assert claim2.status_code == 409
    assert 'already been claimed by another volunteer' in claim2.get_json()['message']

    # The task should now be removed from open tasks
    v2_tasks_after = client.get('/api/volunteer/available-tasks', headers=auth(vol2)).get_json()['tasks']
    assert not any(t['request_id'] == request_id for t in v2_tasks_after)

    # Volunteer 1 now carries out pickup and delivery
    st, _ = set_status(client, vol1, assign_id, 'PICKED_UP')
    assert st == 200

    st, _ = set_status(client, vol1, assign_id, 'OUT_FOR_DELIVERY')
    assert st == 200

    st, _ = upload_proof(client, vol1, assign_id)
    assert st == 200

    # NGO confirms delivery with beneficiary count
    confirm = client.post('/api/ngo/confirm-delivery', json={
        'delivery_id': assign_id,
        'beneficiary_count': 35,
        'beneficiary_notes': 'Meals served to 35 shelter residents.'
    }, headers=auth(ngo))
    assert confirm.status_code == 200
    assert confirm.get_json()['delivery']['status'] == 'COMPLETED'
    assert confirm.get_json()['delivery']['beneficiary_count'] == 35
