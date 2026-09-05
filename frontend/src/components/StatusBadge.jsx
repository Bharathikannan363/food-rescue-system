import React from 'react';

const StatusBadge = ({ status }) => {
  const getStyle = (st) => {
    switch (st?.toUpperCase()) {
      case 'PENDING':
      case 'PENDING_ADMIN_APPROVAL':
        return 'bg-amber-50 text-amber-700 border-amber-200';
      case 'APPROVED':
      case 'ACCEPTED':
      case 'DONOR_ACCEPTED':
        return 'bg-emerald-50 text-emerald-700 border-emerald-200';
      case 'NGO_REQUESTED':
        return 'bg-blue-50 text-blue-700 border-blue-200';
      case 'VOLUNTEER_ASSIGNED':
      case 'ASSIGNED':
        return 'bg-indigo-50 text-indigo-700 border-indigo-200';
      case 'PICKED_UP':
        return 'bg-purple-50 text-purple-700 border-purple-200';
      case 'OUT_FOR_DELIVERY':
        return 'bg-sky-50 text-sky-700 border-sky-200';
      case 'DELIVERED':
      case 'COMPLETED':
      case 'SUCCESS':
        return 'bg-emerald-100 text-emerald-800 border-emerald-300';
      case 'REJECTED':
      case 'DEACTIVATED':
      case 'CANCELLED':
      case 'FAILED':
        return 'bg-rose-50 text-rose-700 border-rose-200';
      default:
        return 'bg-slate-50 text-slate-700 border-slate-200';
    }
  };

  return (
    <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-semibold border ${getStyle(status)}`}>
      {status?.replace(/_/g, ' ')}
    </span>
  );
};

export default StatusBadge;
