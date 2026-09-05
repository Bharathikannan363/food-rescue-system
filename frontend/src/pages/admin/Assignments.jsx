import React, { useState, useEffect } from 'react';
import { adminService } from '../../services/adminService';
import DataTable from '../../components/DataTable';
import StatusBadge from '../../components/StatusBadge';
import Button from '../../components/Button';
import Modal from '../../components/Modal';
import Loading from '../../components/Loading';
import ErrorMessage from '../../components/ErrorMessage';

const AdminAssignments = () => {
  const [assignments, setAssignments] = useState([]);
  const [requests, setRequests] = useState([]);
  const [volunteers, setVolunteers] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const [modalOpen, setModalOpen] = useState(false);
  const [selectedReqId, setSelectedReqId] = useState('');
  const [selectedVolId, setSelectedVolId] = useState('');

  const fetchData = async () => {
    try {
      setLoading(true);
      const [assignRes, reqRes, volRes] = await Promise.all([
        adminService.getAssignments(),
        adminService.getRequests(),
        adminService.getVolunteers()
      ]);
      if (assignRes.success) setAssignments(assignRes.assignments);
      if (reqRes.success) setRequests(reqRes.requests.filter(r => r.status === 'ACCEPTED'));
      if (volRes.success) setVolunteers(volRes.volunteers.filter(v => v.approval_status === 'APPROVED'));
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchData();
  }, []);

  const handleAssignSubmit = async (e) => {
    e.preventDefault();
    if (!selectedReqId || !selectedVolId) return alert('Select both request and volunteer.');

    try {
      await adminService.assignVolunteer(selectedReqId, selectedVolId);
      setModalOpen(false);
      fetchData();
    } catch (err) {
      alert('Error assigning volunteer: ' + err.message);
    }
  };

  const columns = [
    { header: 'Donation', accessor: 'request_details', cell: (r) => <span className="font-bold text-slate-800">{r.request_details?.donation_title || 'Food Pickup'}</span> },
    { header: 'Assigned Volunteer', accessor: 'volunteer_name', cell: (r) => <span className="font-medium text-slate-700">{r.volunteer_name} ({r.vehicle_type || 'Bike'})</span> },
    { header: 'NGO', accessor: 'request_details', cell: (r) => r.request_details?.ngo_name || 'NGO' },
    { header: 'Status', accessor: 'status', cell: (r) => <StatusBadge status={r.status} /> },
    { header: 'Assigned Date', accessor: 'assigned_at', cell: (r) => new Date(r.assigned_at).toLocaleDateString() }
  ];

  if (loading) return <Loading text="Loading Volunteer Assignments..." />;
  if (error) return <ErrorMessage message={error} retry={fetchData} />;

  return (
    <div className="space-y-6">
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h2 className="text-2xl font-bold text-slate-800">Volunteer Assignments</h2>
          <p className="text-xs text-slate-500 mt-0.5">Assign approved volunteers to NGO accepted food requests</p>
        </div>
        <Button onClick={() => setModalOpen(true)}>
          Assign New Volunteer
        </Button>
      </div>

      <DataTable columns={columns} data={assignments} emptyText="No active assignments." />

      <Modal isOpen={modalOpen} onClose={() => setModalOpen(false)} title="Assign Volunteer to Request">
        <form onSubmit={handleAssignSubmit} className="space-y-4">
          <div>
            <label className="block text-xs font-semibold text-slate-700 uppercase mb-1">Select Accepted Food Request</label>
            <select
              value={selectedReqId}
              onChange={(e) => setSelectedReqId(e.target.value)}
              className="w-full px-3.5 py-2 bg-slate-50 border border-slate-200 rounded-xl text-sm focus:outline-none focus:border-emerald-500 font-medium"
              required
            >
              <option value="">-- Choose Accepted Request --</option>
              {requests.map(r => (
                <option key={r.id} value={r.id}>
                  {r.donation_title} → {r.ngo_name} ({r.donor_name})
                </option>
              ))}
            </select>
          </div>

          <div>
            <label className="block text-xs font-semibold text-slate-700 uppercase mb-1">Select Approved Volunteer</label>
            <select
              value={selectedVolId}
              onChange={(e) => setSelectedVolId(e.target.value)}
              className="w-full px-3.5 py-2 bg-slate-50 border border-slate-200 rounded-xl text-sm focus:outline-none focus:border-emerald-500 font-medium"
              required
            >
              <option value="">-- Choose Volunteer --</option>
              {volunteers.map(v => (
                <option key={v.id} value={v.id}>
                  {v.full_name} ({v.vehicle_type}) - Phone: {v.phone}
                </option>
              ))}
            </select>
          </div>

          <div className="flex items-center justify-end gap-3 pt-2">
            <Button variant="secondary" onClick={() => setModalOpen(false)}>Cancel</Button>
            <Button type="submit">Assign Volunteer</Button>
          </div>
        </form>
      </Modal>
    </div>
  );
};

export default AdminAssignments;
