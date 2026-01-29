import React, { useState, useEffect } from 'react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import { api } from '@/services/api';
import { DashboardStats, TrendingData } from '@/types';
import { DashboardCharts } from '@/components/DashboardCharts';

export const AdminDashboard: React.FC = () => {
  const [stats, setStats] = useState<DashboardStats | null>(null);
  const [trending, setTrending] = useState<TrendingData | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadDashboardData();
  }, []);

  const loadDashboardData = async () => {
    try {
      const [statsResponse, trendingResponse] = await Promise.all([
        api.getDashboardStats(),
        api.getTrendingData(),
      ]);
      setStats(statsResponse.data);
      setTrending(trendingResponse.data);
    } catch (error) {
      console.error('Error loading dashboard:', error);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return <div className="flex items-center justify-center h-screen">Loading...</div>;
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="max-w-7xl mx-auto px-4 py-8">
        <h1 className="text-3xl font-bold text-gray-800 mb-8">👨‍💼 Admin Dashboard</h1>

        {/* Key Metrics */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
          <div className="card p-6 bg-gradient-to-br from-blue-50 to-blue-100">
            <h3 className="text-gray-600 text-sm font-medium mb-2">Total Uploads</h3>
            <p className="text-4xl font-bold text-blue-600">{stats?.total_uploads || 0}</p>
          </div>
          <div className="card p-6 bg-gradient-to-br from-green-50 to-green-100">
            <h3 className="text-gray-600 text-sm font-medium mb-2">Cloth Types</h3>
            <p className="text-4xl font-bold text-green-600">{stats?.cloth_types.length || 0}</p>
          </div>
          <div className="card p-6 bg-gradient-to-br from-purple-50 to-purple-100">
            <h3 className="text-gray-600 text-sm font-medium mb-2">Occasions</h3>
            <p className="text-4xl font-bold text-purple-600">{stats?.occasions.length || 0}</p>
          </div>
        </div>

        {/* Charts */}
        {stats && <DashboardCharts clothTypes={stats.cloth_types} occasions={stats.occasions} />}

        {/* Trending Section */}
        {trending && (
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mt-8">
            {/* Trending Colors */}
            <div className="card p-6">
              <h3 className="text-lg font-semibold text-gray-800 mb-4">🎨 Trending Colors</h3>
              <div className="space-y-2">
                {trending.trending_colors.map((color, idx) => (
                  <div key={idx} className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
                    <span className="text-gray-700 font-medium">{color}</span>
                    <div className="w-8 h-8 rounded border border-gray-200" />
                  </div>
                ))}
              </div>
            </div>

            {/* Trending Patterns */}
            <div className="card p-6">
              <h3 className="text-lg font-semibold text-gray-800 mb-4">✨ Trending Patterns</h3>
              <div className="space-y-2">
                {trending.trending_patterns.map((pattern, idx) => (
                  <div key={idx} className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
                    <span className="text-gray-700 font-medium">{pattern}</span>
                    <span className="text-gray-400">✓</span>
                  </div>
                ))}
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default AdminDashboard;
