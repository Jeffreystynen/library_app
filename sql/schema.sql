-- Library App Database Schema
-- POC with fictitious data

-- Authors table
CREATE TABLE IF NOT EXISTS authors (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    biography TEXT,
    country VARCHAR(100),
    website_url VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Books table
CREATE TABLE IF NOT EXISTS books (
    id SERIAL PRIMARY KEY,
    isbn VARCHAR(20),
    title VARCHAR(255) NOT NULL,
    author_id INTEGER NOT NULL REFERENCES authors(id) ON DELETE CASCADE,
    publication_year INTEGER,
    genre TEXT[], -- Array of genres
    description TEXT,
    cover_url VARCHAR(255),
    pages INTEGER NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Book status tracking (reading progress, ratings, etc.)
CREATE TABLE IF NOT EXISTS book_status (
    id SERIAL PRIMARY KEY,
    book_id INTEGER NOT NULL UNIQUE REFERENCES books(id) ON DELETE CASCADE,
    status VARCHAR(50) DEFAULT 'unread', -- unread, reading, completed, dnf (did not finish)
    date_added TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    date_started TIMESTAMP,
    date_completed TIMESTAMP,
    rating INTEGER CHECK (rating >= 1 AND rating <= 5), -- 1-5 star rating
    is_tbr BOOLEAN DEFAULT FALSE,
    notes TEXT,
    pages_read INTEGER DEFAULT 0,
    reading_speed_estimate DECIMAL(5, 2), -- pages per day
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Reviews table
CREATE TABLE IF NOT EXISTS reviews (
    id SERIAL PRIMARY KEY,
    book_id INTEGER NOT NULL UNIQUE REFERENCES books(id) ON DELETE CASCADE,
    rating INTEGER NOT NULL CHECK (rating >= 1 AND rating <= 5),
    title VARCHAR(255),
    content TEXT NOT NULL,
    spoiler_warning BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Reading sessions (detailed tracking for ML training)
CREATE TABLE IF NOT EXISTS reading_sessions (
    id SERIAL PRIMARY KEY,
    book_id INTEGER NOT NULL REFERENCES books(id) ON DELETE CASCADE,
    session_date DATE NOT NULL,
    pages_read INTEGER NOT NULL,
    duration_minutes INTEGER,
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- TBR List (To-Be-Read)
CREATE TABLE IF NOT EXISTS tbr_list (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- TBR List items (many-to-many)
CREATE TABLE IF NOT EXISTS tbr_items (
    id SERIAL PRIMARY KEY,
    tbr_list_id INTEGER NOT NULL REFERENCES tbr_list(id) ON DELETE CASCADE,
    book_id INTEGER NOT NULL REFERENCES books(id) ON DELETE CASCADE,
    priority INTEGER DEFAULT 0,
    added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(tbr_list_id, book_id)
);

-- Preferences/Settings
CREATE TABLE IF NOT EXISTS preferences (
    id SERIAL PRIMARY KEY,
    key VARCHAR(100) NOT NULL UNIQUE,
    value TEXT,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create indexes for common queries
CREATE INDEX IF NOT EXISTS idx_books_author_id ON books(author_id);
CREATE INDEX IF NOT EXISTS idx_book_status_status ON book_status(status);
CREATE INDEX IF NOT EXISTS idx_book_status_is_tbr ON book_status(is_tbr);
CREATE INDEX IF NOT EXISTS idx_reading_sessions_book_id ON reading_sessions(book_id);
CREATE INDEX IF NOT EXISTS idx_reading_sessions_date ON reading_sessions(session_date);
