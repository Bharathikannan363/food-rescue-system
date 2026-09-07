"""Proximity matcher: nearest-first ranking from live GPS pings."""
from tests.helpers import auth


def test_nearby_volunteers_ranked_nearest_first(client, tokens):
    admin = tokens('admin')
    r = client.get('/api/admin/donations', headers=auth(admin))
    donation = [d for d in r.get_json()['donations'] if d['title'] == 'Seed Fresh'][0]

    r = client.get(f"/api/admin/donations/{donation['id']}/nearby-volunteers", headers=auth(admin))
    assert r.status_code == 200
    body = r.get_json()
    assert body['pickup'] == {'latitude': 28.6139, 'longitude': 77.209}

    vs = body['volunteers']
    assert len(vs) == 3
    # Alex (~0.84 km ping) before Priya (~1.51 km ping); Ravi (no location) last
    assert [v['full_name'] for v in vs] == ['Alex Rivera', 'Priya Sharma', 'Ravi Kumar']
    assert vs[0]['distance_km'] < vs[1]['distance_km']
    assert vs[0]['has_ping'] and vs[1]['has_ping'] and not vs[2]['has_ping']
    assert vs[2]['distance_km'] is None


def test_nearby_volunteers_unknown_donation_404(client, tokens):
    r = client.get('/api/admin/donations/999999/nearby-volunteers', headers=auth(tokens('admin')))
    assert r.status_code == 404
