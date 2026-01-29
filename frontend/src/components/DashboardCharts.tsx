import React, { useState } from 'react';
import {
  BarChart,
  Bar,
  PieChart,
  Pie,
  Cell,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
} from 'recharts';

interface DashboardChartsProps {
  clothTypes: Array<{ type: string; count: number }>;
  occasions: Array<{ occasion: string; count: number }>;
}

export const DashboardCharts: React.FC<DashboardChartsProps> = ({ clothTypes, occasions }) => {
  const COLORS = ['#8b5cf6', '#6366f1', '#3b82f6', '#10b981', '#f59e0b', '#ef4444', '#ec4899', '#8b5cf6'];

  return (
    <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
      {/* Bar Chart: Cloth Types */}
      <div className="card p-6">
        <h3 className="text-lg font-semibold text-gray-800 mb-4">📊 Cloth Types Distribution</h3>
        <ResponsiveContainer width="100%" height={300}>
          <BarChart data={clothTypes}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="type" />
            <YAxis />
            <Tooltip />
            <Bar dataKey="count" fill="#8b5cf6" />
          </BarChart>
        </ResponsiveContainer>
      </div>

      {/* Pie Chart: Occasions */}
      <div className="card p-6">
        <h3 className="text-lg font-semibold text-gray-800 mb-4">🎭 Occasions Breakdown</h3>
        <ResponsiveContainer width="100%" height={300}>
          <PieChart>
            <Pie
              data={occasions}
              cx="50%"
              cy="50%"
              labelLine={false}
              label={({ occasion, count }) => `${occasion} (${count})`}
              outerRadius={80}
              fill="#8884d8"
              dataKey="count"
            >
              {occasions.map((entry, index) => (
                <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
              ))}
            </Pie>
            <Tooltip />
          </PieChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
};

export default DashboardCharts;
