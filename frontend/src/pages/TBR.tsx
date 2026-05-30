import React, { useState, useEffect } from 'react';
import { Bookmark, Trash2, ChevronUp, ChevronDown } from 'lucide-react';
import { TBRItem } from '../types';
import { tbrService } from '../services/api';
import { getBookCoverUrl } from '../utils/bookCovers';

export const TBR: React.FC = () => {
  const [tbrList, setTbrList] = useState<TBRItem[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string>('');
  const [draggedItem, setDraggedItem] = useState<number | null>(null);

  useEffect(() => {
    loadTBRList();
  }, []);

  const loadTBRList = async () => {
    try {
      setLoading(true);
      const response = await tbrService.getTBRList();
      setTbrList(response.data.data || []);
    } catch (err) {
      setError('Failed to load TBR list');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleRemoveFromTBR = async (bookId: number) => {
    try {
      await tbrService.removeFromTBR(bookId);
      setTbrList(tbrList.filter((item) => item.book_id !== bookId));
    } catch (err) {
      setError('Failed to remove book from TBR');
      console.error(err);
    }
  };

  const handleMovePriority = async (item: TBRItem, direction: 'up' | 'down') => {
    const currentIndex = tbrList.findIndex((t) => t.id === item.id);
    if (
      (direction === 'up' && currentIndex === 0) ||
      (direction === 'down' && currentIndex === tbrList.length - 1)
    ) {
      return;
    }

    const newList = [...tbrList];
    const swapIndex = direction === 'up' ? currentIndex - 1 : currentIndex + 1;

    [newList[currentIndex].priority, newList[swapIndex].priority] = [
      newList[swapIndex].priority,
      newList[currentIndex].priority,
    ];

    const temp = newList[currentIndex];
    newList[currentIndex] = newList[swapIndex];
    newList[swapIndex] = temp;

    setTbrList(newList);

    try {
      const itemsToUpdate = newList.map((t) => ({
        id: t.id,
        priority: t.priority,
      }));
      await tbrService.reorderTBR(itemsToUpdate);
    } catch (err) {
      console.error('Failed to update priorities', err);
      loadTBRList();
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-gray-50 to-gray-100 flex items-center justify-center">
        <div className="animate-spin">
          <Bookmark className="w-12 h-12 text-purple-600" />
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-50 to-gray-100 py-8">
      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Header */}
        <div className="mb-12">
          <div className="flex items-center space-x-4 mb-4">
            <div className="p-3 bg-gradient-to-br from-amber-400 to-orange-600 rounded-lg">
              <Bookmark className="w-8 h-8 text-white" />
            </div>
            <div>
              <h1 className="text-4xl font-bold text-gray-900">To Be Read</h1>
              <p className="text-gray-600">Your curated reading queue</p>
            </div>
          </div>
        </div>

        {error && (
          <div className="bg-red-50 border border-red-200 rounded-xl p-6 text-red-800 mb-6">
            {error}
          </div>
        )}

        {tbrList.length === 0 ? (
          <div className="bg-white rounded-xl shadow-md p-12 text-center">
            <Bookmark className="w-16 h-16 text-gray-400 mx-auto mb-4" />
            <h2 className="text-2xl font-bold text-gray-900 mb-2">No books in your TBR</h2>
            <p className="text-gray-600">Start adding books from your library to create your reading queue</p>
          </div>
        ) : (
          <div className="space-y-4">
            <p className="text-gray-600 font-medium">
              {tbrList.length} book{tbrList.length !== 1 ? 's' : ''} in your queue
            </p>

            <div className="bg-white rounded-xl shadow-md overflow-hidden">
              {tbrList.map((item, index) => (
                <TBRListItem
                  key={item.id}
                  item={item}
                  index={index}
                  total={tbrList.length}
                  onRemove={handleRemoveFromTBR}
                  onMovePriority={handleMovePriority}
                />
              ))}
            </div>

            {/* Reading Queue Stats */}
            <div className="grid grid-cols-1 sm:grid-cols-3 gap-4 mt-8">
              <div className="bg-gradient-to-br from-blue-500 to-blue-600 rounded-xl p-6 text-white">
                <p className="text-sm opacity-90">Total Pages</p>
                <p className="text-3xl font-bold mt-2">
                  {tbrList.reduce((sum, item) => sum + item.pages, 0).toLocaleString()}
                </p>
              </div>
              <div className="bg-gradient-to-br from-purple-500 to-purple-600 rounded-xl p-6 text-white">
                <p className="text-sm opacity-90">Est. Reading Time</p>
                <p className="text-3xl font-bold mt-2">
                  ~{Math.round(tbrList.reduce((sum, item) => sum + item.pages, 0) / 50)} days
                </p>
              </div>
              <div className="bg-gradient-to-br from-orange-500 to-orange-600 rounded-xl p-6 text-white">
                <p className="text-sm opacity-90">Avg. Pages/Book</p>
                <p className="text-3xl font-bold mt-2">
                  {Math.round(tbrList.reduce((sum, item) => sum + item.pages, 0) / tbrList.length)}
                </p>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

interface TBRListItemProps {
  item: TBRItem;
  index: number;
  total: number;
  onRemove: (bookId: number) => void;
  onMovePriority: (item: TBRItem, direction: 'up' | 'down') => void;
}

const TBRListItem: React.FC<TBRListItemProps> = ({
  item,
  index,
  total,
  onRemove,
  onMovePriority,
}) => {
  const [imageError, setImageError] = useState(false);
  const coverUrl = getBookCoverUrl(item.title);

  return (
    <div
      className={`flex items-center space-x-4 p-6 ${
        index !== total - 1 ? 'border-b border-gray-200' : ''
      } hover:bg-gray-50 transition-colors`}
    >
      {/* Priority Rank */}
      <div className="flex-shrink-0">
        <div className="w-12 h-12 rounded-full bg-gradient-to-br from-amber-400 to-orange-600 flex items-center justify-center text-white font-bold text-lg">
          {index + 1}
        </div>
      </div>

      {/* Book Cover */}
      <div className="flex-shrink-0">
        <img
          src={imageError ? 'data:image/svg+xml,%3Csvg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 150 225"%3E%3Crect fill="%23E5E7EB" width="150" height="225"/%3E%3C/svg%3E' : coverUrl}
          alt={item.title}
          className="w-20 h-32 object-cover rounded-lg shadow-md"
          onError={() => setImageError(true)}
        />
      </div>

      {/* Book Info */}
      <div className="flex-grow">
        <h3 className="text-lg font-bold text-gray-900">{item.title}</h3>
        <p className="text-gray-600">{item.author_name}</p>
        <div className="flex flex-wrap gap-2 mt-3">
          <span className="text-xs bg-blue-100 text-blue-700 px-3 py-1 rounded-full">
            {item.pages} pages
          </span>
          {item.genre?.slice(0, 2).map((g) => (
            <span key={g} className="text-xs bg-purple-100 text-purple-700 px-3 py-1 rounded-full">
              {g}
            </span>
          ))}
        </div>
      </div>

      {/* Actions */}
      <div className="flex items-center space-x-3">
        <div className="flex flex-col space-y-1">
          <button
            onClick={() => onMovePriority(item, 'up')}
            disabled={index === 0}
            className="p-1 text-gray-500 hover:text-gray-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
            title="Move up"
          >
            <ChevronUp className="w-5 h-5" />
          </button>
          <button
            onClick={() => onMovePriority(item, 'down')}
            disabled={index === total - 1}
            className="p-1 text-gray-500 hover:text-gray-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
            title="Move down"
          >
            <ChevronDown className="w-5 h-5" />
          </button>
        </div>
        <button
          onClick={() => onRemove(item.book_id)}
          className="p-2 text-red-500 hover:bg-red-50 rounded-lg transition-colors"
          title="Remove from TBR"
        >
          <Trash2 className="w-5 h-5" />
        </button>
      </div>
    </div>
  );
};
