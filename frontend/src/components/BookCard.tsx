import React, { useState } from 'react';
import { Star } from 'lucide-react';
import { Book } from '../types';
import { getBookCoverUrl } from '../utils/bookCovers';

interface BookCardProps {
  book: Book;
  onClick?: () => void;
}

export const BookCard: React.FC<BookCardProps> = ({ book, onClick }) => {
  const [imageError, setImageError] = useState(false);
  const coverUrl = getBookCoverUrl(book.title);

  const getStatusColor = (status?: string) => {
    switch (status) {
      case 'completed':
        return 'bg-emerald-500';
      case 'reading':
        return 'bg-blue-500';
      case 'tbr':
        return 'bg-amber-500';
      default:
        return 'bg-gray-500';
    }
  };

  return (
    <div
      onClick={onClick}
      className="group cursor-pointer h-full"
    >
      <div className="bg-white rounded-xl overflow-hidden shadow-md hover:shadow-2xl transition-all duration-300 hover:scale-105 h-full flex flex-col">
        {/* Book Cover */}
        <div className="relative overflow-hidden bg-gradient-to-br from-purple-200 to-blue-200 aspect-[2/3]">
          <img
            src={imageError ? 'data:image/svg+xml,%3Csvg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 300 450"%3E%3Crect fill="%23E5E7EB" width="300" height="450"/%3E%3Ctext x="50%" y="50%" font-size="24" fill="%236B7280" text-anchor="middle" dominant-baseline="middle"%3EBook Cover%3C/text%3E%3C/svg%3E' : coverUrl}
            alt={book.title}
            className="w-full h-full object-cover group-hover:scale-110 transition-transform duration-300"
            onError={() => setImageError(true)}
          />
          {book.status && (
            <div className={`absolute top-2 right-2 px-3 py-1 rounded-full text-white text-xs font-bold ${getStatusColor(book.status)}`}>
              {book.status === 'reading' ? 'Reading' : book.status.charAt(0).toUpperCase() + book.status.slice(1)}
            </div>
          )}
        </div>

        {/* Book Info */}
        <div className="p-4 flex flex-col flex-grow">
          <h3 className="font-bold text-sm text-gray-900 line-clamp-2 mb-1">
            {book.title}
          </h3>
          <p className="text-xs text-gray-600 mb-3 flex-grow">
            {book.author_name}
          </p>

          {/* Rating */}
          {book.rating && (
            <div className="flex items-center space-x-1 mb-3">
              <div className="flex">
                {[...Array(5)].map((_, i) => (
                  <Star
                    key={i}
                    className={`w-3 h-3 ${
                      i < Math.round(book.rating || 0)
                        ? 'fill-yellow-400 text-yellow-400'
                        : 'text-gray-300'
                    }`}
                  />
                ))}
              </div>
              <span className="text-xs text-gray-600">{book.rating}</span>
            </div>
          )}

          {/* Progress */}
          {book.status === 'reading' && book.pages && book.pages_read && (
            <div className="mb-3">
              <div className="w-full bg-gray-200 rounded-full h-2">
                <div
                  className="bg-gradient-to-r from-blue-500 to-cyan-500 h-2 rounded-full transition-all"
                  style={{ width: `${(book.pages_read / book.pages) * 100}%` }}
                />
              </div>
              <p className="text-xs text-gray-600 mt-1">
                {book.pages_read} / {book.pages} pages
              </p>
            </div>
          )}

          {/* Genres */}
          <div className="flex flex-wrap gap-1">
            {book.genre?.slice(0, 2).map((g) => (
              <span
                key={g}
                className="text-xs bg-purple-100 text-purple-700 px-2 py-1 rounded-full"
              >
                {g}
              </span>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
};
