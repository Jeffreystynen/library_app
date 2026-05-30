import axios from 'axios';
import { Book, Stats, TBRItem, ApiResponse } from '../types';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000/api';

const api = axios.create({
  baseURL: API_BASE_URL,
});

export const bookService = {
  getBooks: (limit = 50, offset = 0) =>
    api.get<ApiResponse<Book[]>>('/books', { params: { limit, offset } }),

  getBook: (id: number) =>
    api.get<ApiResponse<Book>>(`/books/${id}`),

  searchBooks: (query: string) =>
    api.get<ApiResponse<Book[]>>('/books/search', { params: { q: query } }),

  getBookStatus: (id: number) =>
    api.get(`/books/${id}/status`),

  updateRating: (id: number, rating: number) =>
    api.put(`/books/${id}/rating`, { rating }),

  updateProgress: (id: number, pages_read: number) =>
    api.put(`/books/${id}/progress`, { pages_read }),

  updateStatus: (id: number, status: string) =>
    api.put(`/books/${id}/status`, { status }),
};

export const statsService = {
  getStats: () =>
    api.get<ApiResponse<Stats>>('/stats'),
};

export const tbrService = {
  getTBRList: () =>
    api.get<ApiResponse<TBRItem[]>>('/tbr'),

  addToTBR: (bookId: number, priority = 0) =>
    api.post(`/tbr/${bookId}`, { priority }),

  removeFromTBR: (bookId: number) =>
    api.delete(`/tbr/${bookId}`),

  reorderTBR: (items: { id: number; priority: number }[]) =>
    api.put('/tbr/order', { items }),
};

export default api;
