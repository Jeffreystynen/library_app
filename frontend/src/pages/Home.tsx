import React, { useState, useEffect } from 'react';
import { BookOpen, Search, Calendar } from 'lucide-react';
import { Book } from '../types';
import { bookService } from '../services/api';
import { BookCard } from '../components/BookCard';

interface Prediction {
  book_id: number;
  title: string;
  estimated_finish_date: string;
  days_remaining: number;
  predicted_pages_per_day: number;
}

export const Home: React.FC = () => {
  const [books, setBooks] = useState<Book[]>([]);
  const [filteredBooks, setFilteredBooks] = useState<Book[]>([]);
  const [searchQuery, setSearchQuery] = useState('');
  const [statusFilter, setStatusFilter] = useState<string>('all');
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string>('');
  const [predictions, setPredictions] = useState<Prediction[]>([]);

  useEffect(() => {
    loadBooks();
  }, []);

  useEffect(() => {
    filterBooks();
  }, [books, searchQuery, statusFilter]);

  useEffect(() => {
    loadPredictions();
  }, [books]);

  const loadBooks = async () => {
    try {
      setLoading(true);
      const response = await bookService.getBooks(50, 0);
      setBooks(response.data.data || []);
    } catch (err) {
      setError('Failed to load books');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const loadPredictions = async () => {
    try {
      const readingBooks = books.filter((b) => b.status === 'reading');
      const preds: Prediction[] = [];

      for (const book of readingBooks) {
        try {
          const response = await bookService.getBook(book.id);
          const predResponse = await fetch(`/api/books/${book.id}/prediction`);
          if (predResponse.ok) {
            const predData = await predResponse.json();
            if (predData.data) {
              preds.push(predData.data);
            }
          }
        } catch (err) {
          console.error(`Failed to load prediction for book ${book.id}`);
        }
      }

      setPredictions(preds);
    } catch (err) {
      console.error('Failed to load predictions');
    }
  };

  const filterBooks = () => {
    let filtered = books;

    if (statusFilter !== 'all') {
      filtered = filtered.filter((book) => book.status === statusFilter);
    }

    if (searchQuery) {
      filtered = filtered.filter(
        (book) =>
          book.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
          book.author_name.toLowerCase().includes(searchQuery.toLowerCase())
      );
    }

    setFilteredBooks(filtered);
  };

  const stats = {
    total: books.length,
    completed: books.filter((b) => b.status === 'completed').length,
    reading: books.filter((b) => b.status === 'reading').length,
    tbr: books.filter((b) => b.status === 'tbr').length,
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-50 to-gray-100 py-8">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Hero Section */}
        <div className="mb-12">
          <div className="bg-gradient-to-r from-purple-600 via-purple-700 to-indigo-700 rounded-2xl shadow-xl p-8 sm:p-12 text-white">
            <div className="flex items-center space-x-4 mb-4">
              <BookOpen className="w-12 h-12" />
              <h1 className="text-4xl sm:text-5xl font-bold">My Library</h1>
            </div>
            <p className="text-purple-100 text-lg mb-6">
              A curated collection of literary classics and modern masterpieces
            </p>

            {/* Quick Stats */}
            <div className="grid grid-cols-2 sm:grid-cols-4 gap-4">
              <StatItem label="Books" value={stats.total} />
              <StatItem label="Read" value={stats.completed} />
              <StatItem label="Reading" value={stats.reading} />
              <StatItem label="To Read" value={stats.tbr} />
            </div>
          </div>
        </div>

        {/* Currently Reading with Predictions */}
        {predictions.length > 0 && (
          <div className="mb-12">
            <h2 className="text-2xl font-bold text-gray-900 mb-4">Currently Reading</h2>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              {predictions.map((pred) => (
                <div key={pred.book_id} className="bg-white rounded-xl shadow-md overflow-hidden hover:shadow-lg transition-shadow">
                  <div className="bg-gradient-to-r from-blue-500 to-cyan-500 p-6 text-white">
                    <h3 className="text-lg font-bold mb-2">{pred.title}</h3>
                    <div className="flex items-center space-x-2 mb-3">
                      <Calendar className="w-4 h-4" />
                      <span className="text-sm">Estimated finish date</span>
                    </div>
                    <p className="text-3xl font-bold">{new Date(pred.estimated_finish_date).toLocaleDateString()}</p>
                  </div>
                  <div className="p-6">
                    <div className="grid grid-cols-2 gap-4">
                      <div>
                        <p className="text-sm text-gray-600 mb-1">Days remaining</p>
                        <p className="text-2xl font-bold text-gray-900">{Math.round(pred.days_remaining)}</p>
                      </div>
                      <div>
                        <p className="text-sm text-gray-600 mb-1">Pages/day</p>
                        <p className="text-2xl font-bold text-gray-900">{pred.predicted_pages_per_day.toFixed(1)}</p>
                      </div>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Search and Filter */}
        <div className="mb-8 space-y-4">
          <div className="relative">
            <Search className="absolute left-4 top-3 text-gray-400 w-5 h-5" />
            <input
              type="text"
              placeholder="Search by title or author..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="w-full pl-12 pr-4 py-3 rounded-xl border border-gray-300 focus:border-purple-500 focus:ring-2 focus:ring-purple-500/20 outline-none transition-all bg-white"
            />
          </div>

          <div className="flex flex-wrap gap-2">
            {['all', 'completed', 'reading', 'tbr', 'unread'].map((filter) => (
              <button
                key={filter}
                onClick={() => setStatusFilter(filter)}
                className={`px-4 py-2 rounded-lg font-medium transition-all ${
                  statusFilter === filter
                    ? 'bg-purple-600 text-white shadow-lg'
                    : 'bg-white text-gray-700 hover:bg-gray-100 border border-gray-300'
                }`}
              >
                {filter.charAt(0).toUpperCase() + filter.slice(1)}
              </button>
            ))}
          </div>
        </div>

        {/* Books Grid */}
        {loading ? (
          <div className="flex justify-center items-center h-64">
            <div className="animate-spin">
              <BookOpen className="w-12 h-12 text-purple-600" />
            </div>
          </div>
        ) : error ? (
          <div className="bg-red-50 border border-red-200 rounded-xl p-6 text-red-800">
            {error}
          </div>
        ) : (
          <>
            <p className="text-gray-600 mb-6">
              Showing {filteredBooks.length} of {books.length} books
            </p>
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
              {filteredBooks.map((book) => (
                <BookCard key={book.id} book={book} />
              ))}
            </div>

            {filteredBooks.length === 0 && (
              <div className="text-center py-12">
                <BookOpen className="w-16 h-16 text-gray-400 mx-auto mb-4" />
                <p className="text-gray-600 text-lg">No books found</p>
              </div>
            )}
          </>
        )}
      </div>
    </div>
  );
};

const StatItem: React.FC<{ label: string; value: number }> = ({ label, value }) => (
  <div className="bg-white/20 rounded-lg p-4 text-center backdrop-blur">
    <p className="text-purple-100 text-sm">{label}</p>
    <p className="text-3xl font-bold mt-1">{value}</p>
  </div>
);
