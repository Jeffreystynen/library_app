export interface Book {
  id: number;
  title: string;
  author_name: string;
  author_id: number;
  isbn: string;
  publication_year: number;
  genre: string[];
  description: string;
  cover_url?: string;
  pages: number;
  status?: 'unread' | 'reading' | 'completed' | 'dnf' | 'tbr';
  rating?: number;
  pages_read?: number;
  date_started?: string;
  date_completed?: string;
  is_tbr?: boolean;
  notes?: string;
}

export interface BookStatus {
  status: 'unread' | 'reading' | 'completed' | 'dnf' | 'tbr';
  rating?: number;
  pages_read: number;
  date_started?: string;
  date_completed?: string;
  notes?: string;
}

export interface Stats {
  total_books: number;
  by_status: { status: string; count: number }[];
  by_genre: { genre: string; count: number }[];
  by_rating: { rating: number; count: number }[];
  average_rating: { average_rating: string; reviewed_books: number };
  pages_statistics: {
    total_books_read: number;
    total_pages_started: number;
    average_book_length: string;
  };
  top_authors: { name: string; count: number }[];
  progress: {
    completed_books: number;
    books_reading: number;
    unread_books: number;
    tbr_count: number;
    rated_books: number;
  };
}

export interface TBRItem {
  id: number;
  book_id: number;
  title: string;
  author_name: string;
  pages: number;
  genre: string[];
  priority: number;
  status: string;
}

export interface ApiResponse<T> {
  status: string;
  data?: T;
  message?: string;
}
