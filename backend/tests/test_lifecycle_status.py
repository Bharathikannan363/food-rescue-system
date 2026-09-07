"""Full lifecycle happy path and delivery status order enforcement."""
from tests.helpers import auth, post_food, run_lifecycle, set_status


def test_full_lifecycle_happy_path(client, tokens, admin_can_assign=None):
    donor, ngo, admin, vol = tokens('donor'), tokens('ngo'), tokens('admin'), tokens('volunteer')
    st, body = post_food(client, donor, title='Lifecycle Food', expiry_minutes=300)
    assert st == 201 and body['donation']['expiry_state'] == 'FRESH'

    flow = run_lifecycle(client, donor, ngo, admin, vol, body['donation']['id'])
    aid = flow['assignment_id']

    st, _ = set_status(client, vol, aid, 'PICKED_UP')
    assert st == 200
    st, _ = set_status(client, vol, aid, 'OUT_FOR_DELIVERY')
    assert st == 200
    st, body = set_status(client, vol, aid, 'DELIVERED')
    assert st == 200

    r = client.post('/api/ngo/confirm-delivery',
                    json={'delivery_id': aid, 'beneficiary_count': 9,
                          'beneficiary_notes': 'test'}, headers=auth(ngo))
    assert r.status_code == 200
    assert r.get_json()['delivery']['status'] == 'COMPLETED'


def test_assign_response_includes_pickup_distance(client, tokens):
    """Proximity data reaches the assignment record."""
    donor, ngo, admin, vol = tokens('donor'), tokens('ngo'), tokens('admin'), tokens('volunteer')
    _, body = post_food(client, donor, title='Distance Food')
    flow = run_lifecycle(client, donor, ngo, admin, vol, body['donation']['id'])
    assert flow['assign_distance'] is not None and flow['assign_distance'] > 0


def test_status_order_enforced(client, tokens):
    """No skipping and no going backwards: every illegal jump is a 400."""
    donor, ngo, admin, vol = tokens('donor'), tokens('ngo'), tokens('admin'), tokens('volunteer')
    _, body = post_food(client, donor, title='Order Food')
    flow = run_lifecycle(client, donor, ngo, admin, vol, body['donation']['id'])
    aid = flow['assignment_id']

    # From ASSIGNED/ACCEPTED: cannot skip straight to later stages
    st, msg = set_status(client, vol, aid, 'DELIVERED')
    assert st == 400 and 'Invalid status transition' in msg['message']
    st, _ = set_status(client, vol, aid, 'OUT_FOR_DELIVERY')
    assert st == 400

    assert set_status(client, vol, aid, 'PICKED_UP')[0] == 200
    # No repeats / backwards / unknown statuses
    st, _ = set_status(client, vol, aid, 'PICKED_UP')
    assert st == 400
    st, _ = set_status(client, vol, aid, 'DELIVERED')
    assert st == 400
    st, _ = set_status(client, vol, aid, 'NOT_A_STATUS')
    assert st == 400

    assert set_status(client, vol, aid, 'OUT_FOR_DELIVERY')[0] == 200
    st, _ = set_status(client, vol, aid, 'PICKED_UP')
    assert st == 400

    assert set_status(client, vol, aid, 'DELIVERED')[0] == 200
