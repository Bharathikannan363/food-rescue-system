import React, { useState, useEffect } from 'react';
import { donorService } from '../../services/donorService';
import DataTable from '../../components/DataTable';
import StatusBadge from '../../components/StatusBadge';
import Button from '../../components/Button';
import Loading from '../../components/Loading';
import ErrorMessage from '../../components/ErrorMessage';
import { Clock, Ban } from 'lucide-react';

const MyDonations = () => {
  const [donations, setDonations] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const fetchDonations = async () => {
    try {
      setLoading(true);
      const res = await donorService.getMyDonations();
      if (res.success) setDonations(res.donations);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchDonations();
  }, []);

  const handleCancel = async (donationId) => {
    try {
      const res = await donorService.cancelDonation(donationId);
      if (res.success) {
        alert('Donation cancelled successfully.');
        fetchDonations();
      }
    } catch (err) {
      alert(err.message);
    }
  };

  const isWithin20Mins = (createdAt) => {
    if (!createdAt) return false;
    const createdTime = new Date(createdAt).getTime();
    const now = new Date().getTime();
    const diffMinutes = (now - createdTime) / (1000 * 60);
    return diffMinutes <= 20;
  };

  const columns = [
    { header: 'Food Title', accessor: 'title', cell: (r) => <span className="font-bold text-slate-800">{r.title}</span> },
    { header: 'Category', accessor: 'food_type', cell: (r) => <span className="text-xs bg-slate-100 px-2 py-1 rounded font-semibold">{r.food_type}</span> },
    { header: 'Quantity', accessor: 'quantity' },
    { header: 'Posted Time', accessor: 'created_at', cell: (r) => new Date(r.created_at).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }) },
    { header: 'Status', accessor: 'status', cell: (r) => <StatusBadge status={r.status} /> },
    {
      header: '20-Min Cancellation',
      cell: (r) => {
        const canCancel = isWithin20Mins(r.created_at) && !['PICKED_UP', 'OUT_FOR_DELIVERY', 'DELIVERED', 'COMPLETED', 'CANCELLED'].includes(r.status);
        return (
          <div>
            {r.status === 'CANCELLED' ? (
              <span className="text-xs text-rose-600 font-semibold">Cancelled</span>
            ) : canCancel ? (
              <Button size="sm" variant="danger" icon={Ban} onClick={() => handleCancel(r.id)}>
                Cancel Post
              </Button>
            ) : (
              <span className="text-xs text-slate-400 font-medium flex items-center gap-1">
                <Clock className="w-3.5 h-3.5" /> Window Closed
              </span>
            )}
          </div>
        );
      }
    }
  ];

  if (loading) return <Loading text="Loading My Food Donations..." />;
  if (error) return <ErrorMessage message={error} retry={fetchDonations} />;

  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-2xl font-bold text-slate-800">My Surplus Food Donations</h2>
        <p className="text-xs text-slate-500 mt-0.5">Track your posted donations & manage 20-minute cancellation window</p>
      </div>

      <DataTable columns={columns} data={donations} emptyText="No food donations posted yet." />
    </div>
  );
};

export default MyDonations;
