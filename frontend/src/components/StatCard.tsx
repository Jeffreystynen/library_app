import React from 'react';

interface StatCardProps {
  label: string;
  value: string | number;
  icon: React.ReactNode;
  color: 'purple' | 'blue' | 'emerald' | 'orange' | 'pink' | 'indigo';
  subtext?: string;
}

const colorClasses = {
  purple: 'bg-gradient-to-br from-purple-400 to-purple-600',
  blue: 'bg-gradient-to-br from-blue-400 to-blue-600',
  emerald: 'bg-gradient-to-br from-emerald-400 to-emerald-600',
  orange: 'bg-gradient-to-br from-orange-400 to-orange-600',
  pink: 'bg-gradient-to-br from-pink-400 to-pink-600',
  indigo: 'bg-gradient-to-br from-indigo-400 to-indigo-600',
};

export const StatCard: React.FC<StatCardProps> = ({ label, value, icon, color, subtext }) => {
  return (
    <div className="bg-white rounded-xl shadow-md hover:shadow-lg transition-shadow p-6">
      <div className={`${colorClasses[color]} rounded-lg p-3 w-fit mb-4`}>
        <div className="text-white">{icon}</div>
      </div>
      <p className="text-gray-600 text-sm font-medium">{label}</p>
      <p className="text-3xl font-bold text-gray-900 mt-2">{value}</p>
      {subtext && <p className="text-xs text-gray-500 mt-2">{subtext}</p>}
    </div>
  );
};
