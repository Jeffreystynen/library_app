import React, { useState, useEffect } from 'react';
import {
  PieChart,
  Pie,
  Cell,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
  LineChart,
  Line,
} from 'recharts';
import { BarChart3, BookOpen, Star, TrendingUp, Clock } from 'lucide-react';
import { Stats } from '../types';
import { statsService } from '../services/api';
import { StatCard } from '../components/StatCard';

export const Statistics: React.FC = () => {
  const [stats, setStats] = useState<Stats | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string>('');

  useEffect(() => {
    loadStats();
  }, []);

  const loadStats = async () => {
    try {
      setLoading(true);
      const response = await statsService.getStats();
      setStats(response.data.data || null);
    } catch (err) {
      setError('Failed to load statistics');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-gray-50 to-gray-100 flex items-center justify-center">
        <div className="animate-spin">
          <BarChart3 className="w-12 h-12 text-purple-600" />
        </div>
      </div>
    );
  }

  if (error || !stats) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-gray-50 to-gray-100 py-8">
        <div className="max-w-7xl mx-auto px-4">
          <div className="bg-red-50 border border-red-200 rounded-xl p-6 text-red-800">
            {error}
          </div>
        </div>
      </div>
    );
  }

  const completionPercentage = stats.progress.completed_books
    ? Math.round((stats.progress.completed_books / stats.total_books) * 100)
    : 0;

  const avgRating = stats.average_rating.average_rating
    ? parseFloat(stats.average_rating.average_rating)
    : 0;

  const colors = ['#8B5CF6', '#6366F1', '#06B6D4', '#10B981', '#F59E0B', '#EF4444'];

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-50 to-gray-100 py-8">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Header */}
        <div className="mb-12">
          <h1 className="text-4xl font-bold text-gray-900 mb-2">Reading Statistics</h1>
          <p className="text-gray-600">Insights into your literary journey</p>
        </div>

        {/* Key Metrics */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-5 gap-6 mb-12">
          <StatCard
            label="Total Books"
            value={stats.total_books}
            icon={<BookOpen className="w-6 h-6" />}
            color="purple"
          />
          <StatCard
            label="Completed"
            value={stats.progress.completed_books}
            icon={<TrendingUp className="w-6 h-6" />}
            color="emerald"
            subtext={`${completionPercentage}% of library`}
          />
          <StatCard
            label="Currently Reading"
            value={stats.progress.books_reading}
            icon={<BookOpen className="w-6 h-6" />}
            color="blue"
          />
          <StatCard
            label="Average Rating"
            value={avgRating.toFixed(1)}
            icon={<Star className="w-6 h-6" />}
            color="orange"
            subtext={`${stats.average_rating.reviewed_books} rated`}
          />
          <StatCard
            label="Total Pages Read"
            value={stats.pages_statistics.total_pages_started.toLocaleString()}
            icon={<Clock className="w-6 h-6" />}
            color="pink"
          />
        </div>

        {/* Charts Grid */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-12">
          {/* Reading Status Distribution */}
          <div className="bg-white rounded-xl shadow-md p-6">
            <h2 className="text-xl font-bold text-gray-900 mb-6">Reading Status</h2>
            <ResponsiveContainer width="100%" height={300}>
              <PieChart>
                <Pie
                  data={stats.by_status}
                  cx="50%"
                  cy="50%"
                  labelLine={false}
                  label={({ status, count }) => `${status}: ${count}`}
                  outerRadius={100}
                  fill="#8884d8"
                  dataKey="count"
                >
                  {stats.by_status.map((_, index) => (
                    <Cell key={`cell-${index}`} fill={colors[index % colors.length]} />
                  ))}
                </Pie>
                <Tooltip />
              </PieChart>
            </ResponsiveContainer>
          </div>

          {/* Genre Distribution */}
          <div className="bg-white rounded-xl shadow-md p-6">
            <h2 className="text-xl font-bold text-gray-900 mb-6">Books by Genre</h2>
            <ResponsiveContainer width="100%" height={300}>
              <BarChart
                data={stats.by_genre.slice(0, 6)}
                layout="vertical"
                margin={{ top: 5, right: 30, left: 200, bottom: 5 }}
              >
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis type="number" />
                <YAxis dataKey="genre" type="category" width={180} tick={{ fontSize: 12 }} />
                <Tooltip />
                <Bar dataKey="count" fill="#8B5CF6" radius={[0, 8, 8, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </div>

          {/* Rating Distribution */}
          <div className="bg-white rounded-xl shadow-md p-6">
            <h2 className="text-xl font-bold text-gray-900 mb-6">Rating Distribution</h2>
            <ResponsiveContainer width="100%" height={300}>
              <BarChart data={stats.by_rating}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="rating" />
                <YAxis />
                <Tooltip />
                <Bar dataKey="count" fill="#F59E0B" radius={[8, 8, 0, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </div>

          {/* Top Authors */}
          <div className="bg-white rounded-xl shadow-md p-6">
            <h2 className="text-xl font-bold text-gray-900 mb-6">Top Authors</h2>
            <div className="space-y-4">
              {stats.top_authors.map((author, index) => (
                <div key={index} className="flex items-center justify-between">
                  <div className="flex items-center space-x-3 flex-1">
                    <div className="w-10 h-10 rounded-full bg-gradient-to-br from-purple-400 to-indigo-600 flex items-center justify-center text-white font-bold">
                      {index + 1}
                    </div>
                    <div className="flex-1">
                      <p className="font-semibold text-gray-900">{author.name}</p>
                    </div>
                  </div>
                  <div className="flex items-center space-x-2">
                    <div className="w-32 h-2 bg-gray-200 rounded-full overflow-hidden">
                      <div
                        className="h-full bg-gradient-to-r from-purple-500 to-indigo-600"
                        style={{
                          width: `${(author.count / stats.top_authors[0].count) * 100}%`,
                        }}
                      />
                    </div>
                    <span className="text-sm font-bold text-gray-700 w-8">{author.count}</span>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>

        {/* Reading Progress Overview */}
        <div className="bg-white rounded-xl shadow-md p-6 mb-12">
          <h2 className="text-xl font-bold text-gray-900 mb-6">Library Overview</h2>
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
            <ProgressItem
              label="Completion Rate"
              value={completionPercentage}
              unit="%"
              color="from-emerald-400 to-emerald-600"
            />
            <ProgressItem
              label="Average Book Length"
              value={parseInt(stats.pages_statistics.average_book_length)}
              unit="pages"
              color="from-blue-400 to-blue-600"
            />
            <ProgressItem
              label="Total Pages Covered"
              value={Math.round(
                parseInt(stats.pages_statistics.total_pages_started) / 100
              )}
              unit="00 pages"
              color="from-pink-400 to-pink-600"
            />
            <ProgressItem
              label="Estimated Reading Days"
              value={Math.round(
                parseInt(stats.pages_statistics.total_pages_started) / 50
              )}
              unit="days"
              color="from-orange-400 to-orange-600"
            />
          </div>
        </div>
      </div>
    </div>
  );
};

interface ProgressItemProps {
  label: string;
  value: number;
  unit: string;
  color: string;
}

const ProgressItem: React.FC<ProgressItemProps> = ({ label, value, unit, color }) => (
  <div className={`bg-gradient-to-br ${color} rounded-xl p-6 text-white`}>
    <p className="text-sm font-medium opacity-90">{label}</p>
    <p className="text-3xl font-bold mt-2">
      {value.toLocaleString()}
      <span className="text-lg ml-1">{unit}</span>
    </p>
  </div>
);
