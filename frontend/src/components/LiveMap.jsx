import React from 'react';
import { MapContainer, TileLayer, Marker, Popup } from 'react-leaflet';
import L from 'leaflet';

const volunteerIcon = new L.Icon({
  iconUrl: 'https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-2x-[color].png'.replace('[color]', 'blue'),
  shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/0.7.7/images/marker-shadow.png',
  iconSize: [25, 41],
  iconAnchor: [12, 41],
  popupAnchor: [1, -34],
  shadowSize: [41, 41]
});

const donorIcon = new L.Icon({
  iconUrl: 'https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-2x-[color].png'.replace('[color]', 'green'),
  shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/0.7.7/images/marker-shadow.png',
  iconSize: [25, 41],
  iconAnchor: [12, 41],
  popupAnchor: [1, -34],
  shadowSize: [41, 41]
});

const ngoIcon = new L.Icon({
  iconUrl: 'https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-2x-[color].png'.replace('[color]', 'orange'),
  shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/0.7.7/images/marker-shadow.png',
  iconSize: [25, 41],
  iconAnchor: [12, 41],
  popupAnchor: [1, -34],
  shadowSize: [41, 41]
});

const LiveMap = ({ center = [28.6180, 77.2130], zoom = 12, volunteers = [], donors = [], ngos = [] }) => {
  return (
    <div className="h-96 w-full rounded-2xl overflow-hidden border border-slate-200 shadow-sm relative z-0">
      <MapContainer center={center} zoom={zoom} scrollWheelZoom={false} style={{ height: '100%', width: '100%' }}>
        <TileLayer
          attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        />

        {/* Volunteers */}
        {volunteers.map((v, idx) => (
          <Marker key={`vol-${idx}`} position={[v.latitude || 28.6180, v.longitude || 77.2130]} icon={volunteerIcon}>
            <Popup>
              <div className="text-xs font-sans">
                <p className="font-bold text-blue-700">🚚 Volunteer: {v.full_name}</p>
                <p className="text-slate-600">Vehicle: {v.vehicle_type || 'Bike'}</p>
                <p className="text-slate-500 text-[10px]">Phone: {v.phone || 'N/A'}</p>
              </div>
            </Popup>
          </Marker>
        ))}

        {/* Donors */}
        {donors.map((d, idx) => (
          <Marker key={`donor-${idx}`} position={[d.latitude || 28.6139, d.longitude || 77.2090]} icon={donorIcon}>
            <Popup>
              <div className="text-xs font-sans">
                <p className="font-bold text-emerald-700">🥗 Donor: {d.organization_name || d.title}</p>
                <p className="text-slate-600">{d.address || d.pickup_address}</p>
              </div>
            </Popup>
          </Marker>
        ))}

        {/* NGOs */}
        {ngos.map((n, idx) => (
          <Marker key={`ngo-${idx}`} position={[n.latitude || 28.6250, n.longitude || 77.2180]} icon={ngoIcon}>
            <Popup>
              <div className="text-xs font-sans">
                <p className="font-bold text-amber-700">🏢 NGO: {n.ngo_name}</p>
                <p className="text-slate-600">{n.address}</p>
              </div>
            </Popup>
          </Marker>
        ))}
      </MapContainer>
    </div>
  );
};

export default LiveMap;
