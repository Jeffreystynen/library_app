# Library App - System Design

## 1. Project Overview

A personal library management system that enables users to:
- Maintain a catalog of books in their private library
- Track reading progress and completion status
- Create and manage a "To-Be-Read" (TBR) list
- Write and store personal book reviews
- Receive personalized book recommendations (future)
- Predict reading completion times (future)

### ⚠️ Important: POC with Fictitious Data

This is a **Proof of Concept** implementation:
- All data (books, authors, reviews, reading sessions) is **completely fictional**
- Data is generated for demonstration and testing purposes only
- The ML prediction model (Phase 5) will be trained on **fictional data** as well
- This means we can be loose about data accuracy, consistency, and realism
- The goal is to demonstrate functionality, not data integrity
- Any resemblance to real books/authors/data is purely coincidental
- **NOT suitable for production use with real data**

## 2. High-Level Architecture

```
┌─────────────────────────────────────────────────────────┐
│                   Frontend (React)                       │
│  - Book browsing & search                               │
│  - Reading status management                            │
│  - TBR list management                                  │
│  - Review creation/editing                              │
│  - Dashboard & analytics views                          │
└────────────────────┬────────────────────────────────────┘
                     │ HTTP/REST
                     ↓
┌─────────────────────────────────────────────────────────┐
│              Backend API (Python Flask)                  │
│  - RESTful endpoints for all resources                  │
│  - Business logic & validation                          │
│  - Recommendation engine (future)                       │
│  - ML model predictions (future)                        │
│  - No authentication required                           │
└────────────────────┬────────────────────────────────────┘
                     │ SQL
                     ↓
┌─────────────────────────────────────────────────────────┐
│            Database (PostgreSQL)                         │
│  - Books, Reviews, Reading Progress                     │
│  - TBR lists, Preferences                               │
│  - Historical reading data                              │
└─────────────────────────────────────────────────────────┘
```

### Container Strategy
- **postgres:latest** - PostgreSQL database
- **Custom Python image** - Flask API server
- **Custom Node image** - React dev server (development) / nginx (production)
- **docker-compose** - Orchestration and networking

## 3. Backend Architecture - Class & Sequence Diagrams

### 3a. Class Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                         DATABASE MODELS                          │
└─────────────────────────────────────────────────────────────────┘

         ┌──────────────┐                    ┌──────────────┐
         │    Author    │                    │     Book     │
         ├──────────────┤                    ├──────────────┤
         │ id (PK)      │◄───────has many─── │ id (PK)      │
         │ name         │                    │ isbn         │
         │ biography    │                    │ title        │
         │ country      │                    │ author_id(FK)│
         │ website_url  │                    │ publication_ │
         │              │                    │    year      │
         └──────────────┘                    │ genre[]      │
                                             │ description  │
                                             │ cover_url    │
                                             │ pages        │
                                             │ created_at   │
                                             │ updated_at   │
                                             └──────┬───────┘
                                                    │
                              ┌─────────────────────┼──────────────────┐
                              │                     │                  │
                   ┌──────────▼─────────┐  ┌──────▼──────────┐  ┌───▼─────────┐
                   │   BookStatus       │  │     Review      │  │ReviewSession│
                   ├────────────────────┤  ├─────────────────┤  ├──────────────┤
                   │ id (PK)            │  │ id (PK)         │  │ id (PK)      │
                   │ book_id (FK)       │  │ book_id (FK)    │  │ book_id(FK)  │
                   │ status [enum]      │  │ rating (1-5)    │  │ date         │
                   │ date_added         │  │ title           │  │ pages_read   │
                   │ date_started       │  │ content         │  │ duration_min │
                   │ date_completed     │  │ spoiler_warn.   │  │ notes        │
                   │ rating (1-5)       │  │ created_at      │  └──────────────┘
                   │ is_tbr             │  │ updated_at      │
                   │ notes              │  └─────────────────┘
                   │ pages_read         │
                   │ reading_speed      │
                   └────────────────────┘
```

### 3b. Sequence Diagrams

#### Adding a Book to Library
```
┌─────────────────┐                 ┌──────────────┐                ┌──────────────┐
│  React Frontend │                 │ Flask Backend│                │  PostgreSQL  │
└────────┬────────┘                 └──────┬───────┘                └──────┬───────┘
         │                                  │                               │
         │ POST /api/books                  │                               │
         │ {title, author, pages, genre}   │                               │
         ├─────────────────────────────────►│                               │
         │                                  │ Validate input                │
         │                                  │                               │
         │                                  │ INSERT INTO books             │
         │                                  ├──────────────────────────────►│
         │                                  │                               │
         │                                  │◄──────────────────────────────┤
         │                                  │      Book created (id=123)    │
         │                                  │                               │
         │                                  │ INSERT INTO BookStatus        │
         │                                  │ (book_id=123, status=unread) │
         │                                  ├──────────────────────────────►│
         │                                  │                               │
         │                                  │◄──────────────────────────────┤
         │                                  │      Status created           │
         │ [201 Created, id=123]            │                               │
         │◄─────────────────────────────────┤                               │
         │                                  │                               │
```

#### Starting to Read a Book
```
┌─────────────────┐                 ┌──────────────┐                ┌──────────────┐
│  React Frontend │                 │ Flask Backend│                │  PostgreSQL  │
└────────┬────────┘                 └──────┬───────┘                └──────┬───────┘
         │                                  │                               │
         │ PUT /api/books/123/status        │                               │
         │ {status: "reading"}              │                               │
         ├─────────────────────────────────►│                               │
         │                                  │ Validate status transition    │
         │                                  │                               │
         │                                  │ UPDATE BookStatus             │
         │                                  │ SET status = "reading",       │
         │                                  │     date_started = NOW()      │
         │                                  │ WHERE book_id = 123           │
         │                                  ├──────────────────────────────►│
         │                                  │                               │
         │                                  │◄──────────────────────────────┤
         │                                  │      Update confirmed         │
         │ [200 OK, updated status]         │                               │
         │◄─────────────────────────────────┤                               │
         │                                  │                               │
```

#### Writing a Review
```
┌─────────────────┐                 ┌──────────────┐                ┌──────────────┐
│  React Frontend │                 │ Flask Backend│                │  PostgreSQL  │
└────────┬────────┘                 └──────┬───────┘                └──────┬───────┘
         │                                  │                               │
         │ POST /api/books/123/reviews      │                               │
         │ {rating, title, content}         │                               │
         ├─────────────────────────────────►│                               │
         │                                  │ Validate review data          │
         │                                  │                               │
         │                                  │ INSERT INTO Review            │
         │                                  │ (book_id=123, rating=5, ...)  │
         │                                  ├──────────────────────────────►│
         │                                  │                               │
         │                                  │◄──────────────────────────────┤
         │                                  │   Review created (id=456)     │
         │ [201 Created, id=456]            │                               │
         │◄─────────────────────────────────┤                               │
         │                                  │                               │
```

## 4. Data Model

### Core Entities

#### Book
```
- id (UUID, primary key)
- isbn (unique)
- title
- author_id (FK → Author)
- publication_year
- genre (list/array)
- description
- cover_image_url
- pages
- created_at (when added to library)
- updated_at
```

#### Author
```
- id (UUID, primary key)
- name
- biography
- country
- website_url
- created_at
- updated_at
```

#### BookStatus (Ownership/reading status tracking)
```
- id (UUID, primary key)
- book_id (FK → Book)
- status (enum: unread, reading, completed, dnf)
- date_added (when added to library)
- date_started (nullable)
- date_completed (nullable)
- rating (1-5, nullable)
- is_tbr (boolean)
- notes (text)
- pages_read (int, nullable - for tracking progress)
- reading_speed_estimate (pages/day, nullable - computed)
```

#### Review
```
- id (UUID, primary key)
- book_id (FK → Book)
- rating (1-5)
- title
- content (text)
- spoiler_warning (boolean)
- created_at
- updated_at
```

#### ReadingSession (for detailed tracking - future)
```
- id (UUID, primary key)
- book_id (FK → Book)
- date
- pages_read
- duration_minutes
- notes
```

#### TBRList (explicit lists - future expansion)
```
- id (UUID, primary key)
- name
- description
- created_at
- updated_at
- books (many-to-many with Book)
- priority (for ordering)
```

## 5. API Endpoints

### Books
- `GET /api/books` - List all books in library (with pagination, filters)
- `GET /api/books/{id}` - Get book details
- `POST /api/books` - Add book to library (with ISBN lookup integration)
- `PUT /api/books/{id}` - Update book metadata
- `DELETE /api/books/{id}` - Remove book from library
- `GET /api/books/search` - Search books by title/author/genre
- `GET /api/books/stats` - Reading statistics

### Book Status (Reading Status)
- `GET /api/books/{book_id}/status` - Get book's reading status
- `PUT /api/books/{book_id}/status` - Update reading status
- `PUT /api/books/{book_id}/progress` - Update reading progress (pages)
- `PUT /api/books/{book_id}/rating` - Rate a book
- `PUT /api/books/{book_id}/notes` - Add/update personal notes

### TBR List
- `GET /api/tbr` - Get TBR list
- `POST /api/tbr/{book_id}` - Add book to TBR
- `DELETE /api/tbr/{book_id}` - Remove from TBR
- `PUT /api/tbr/order` - Reorder TBR list

### Reviews
- `GET /api/books/{book_id}/reviews` - Get review for a book (single user)
- `POST /api/books/{book_id}/reviews` - Create or update review
- `DELETE /api/books/{book_id}/reviews` - Delete review

### Future: Recommendations
- `GET /api/recommendations` - Get personalized recommendations
- `GET /api/recommendations/reason/{book_id}` - Explain why book recommended

### Future: Reading Predictions
- `GET /api/books/{book_id}/completion-estimate` - Predict completion date

## 9. Frontend Structure

### Pages
- **Dashboard** - Overview, reading stats, recent activity
- **Library** - Browse all books with filters/search
- **Book Detail** - Full book info, reviews, reading progress
- **TBR List** - Manage to-be-read list with sorting options
- **My Reviews** - View and manage personal reviews
- **Reading Stats** - Analytics and insights
- **Settings** - User preferences and account management

### Components (Reusable)
- BookCard - Display book with basic info
- BookListItem - Detailed book row for lists
- ReviewCard - Display single review
- RatingInput - 5-star rating component
- ReadingStatusBadge - Visual status indicator
- SearchBar - Book search with autocomplete
- FilterPanel - Genre, author, status filters

## 7. Backend Architecture - Flask Application Structure

### 7a. Backend Class Diagram

```
┌────────────────────────────────────────────────────────────────┐
│                    FLASK APPLICATION LAYER                     │
└────────────────────────────────────────────────────────────────┘

                    ┌──────────────────────┐
                    │   create_app()       │
                    │   Factory Function   │
                    └──────────┬───────────┘
                               │
                    ┌──────────▼───────────┐
                    │      Flask App       │
                    │  - config            │
                    │  - db (SQLAlchemy)   │
                    │  - blueprints        │
                    └──────────┬───────────┘
                               │
        ┌──────────────────────┼──────────────────────┐
        │                      │                      │
        ▼                      ▼                      ▼
┌──────────────────┐  ┌──────────────────┐  ┌──────────────────┐
│  Books Blueprint │  │  Status Blueprint│  │ Reviews Blueprint│
│  - GET /books    │  │  - PUT /status   │  │ - POST /reviews  │
│  - POST /books   │  │  - PUT /progress │  │ - GET /reviews   │
│  - DELETE /books │  │  - PUT /rating   │  │ - DELETE /review │
│                  │  │  - PUT /notes    │  │                  │
└──────┬───────────┘  └──────┬───────────┘  └──────┬───────────┘
       │                     │                     │
       │ uses                │ uses                │ uses
       ▼                     ▼                     ▼
┌────────────────────────────────────────────────────────┐
│               DATA ACCESS LAYER (Models)              │
├────────────────────────────────────────────────────────┤
│                                                        │
│  ┌──────────────┐  ┌──────────────┐  ┌────────────┐  │
│  │    Book      │  │    Author    │  │ BookStatus │  │
│  ├──────────────┤  ├──────────────┤  ├────────────┤  │
│  │ id           │  │ id           │  │ id         │  │
│  │ title        │  │ name         │  │ book_id    │  │
│  │ author_id    │  │ biography    │  │ status     │  │
│  │ pages        │◄──┤ website      │  │ rating     │  │
│  │ genre[]      │  │              │  │ pages_read │  │
│  │ description  │  │              │  │ notes      │  │
│  │ cover_url    │  │              │  │            │  │
│  │ created_at   │  │              │  │            │  │
│  │ updated_at   │  │              │  │            │  │
│  └──────┬───────┘  └──────────────┘  └────┬───────┘  │
│         │                                   │         │
│         │          ┌──────────────┐         │         │
│         └─────────►│    Review    │◄────────┘         │
│                    ├──────────────┤                    │
│                    │ id           │                    │
│                    │ book_id(FK)  │                    │
│                    │ rating       │                    │
│                    │ title        │                    │
│                    │ content      │                    │
│                    │ spoiler_warn │                    │
│                    │ created_at   │                    │
│                    │ updated_at   │                    │
│                    └──────────────┘                    │
│                                                        │
│  ┌──────────────────┐      ┌──────────────────┐      │
│  │ ReadingSession   │      │     TBRList      │      │
│  ├──────────────────┤      ├──────────────────┤      │
│  │ id               │      │ id               │      │
│  │ book_id(FK)      │      │ name             │      │
│  │ date             │      │ description      │      │
│  │ pages_read       │      │ created_at       │      │
│  │ duration_minutes │      │ updated_at       │      │
│  │ notes            │      │ books[] (M2M)    │      │
│  │                  │      │                  │      │
│  └──────────────────┘      └──────────────────┘      │
│                                                        │
└────────────────────────────────────────────────────────┘
                               │
                               │ uses
                               ▼
┌────────────────────────────────────────────────────────┐
│           DATABASE LAYER (PostgreSQL)                 │
│  - SQLAlchemy ORM handles SQL generation              │
│  - Alembic manages migrations                         │
└────────────────────────────────────────────────────────┘
```

### 7b. Backend Request Handling Flow

```
HTTP Request
    │
    ▼
┌─────────────────────────────────┐
│   Flask Request Handler         │
│   (route matching)              │
└──────────────┬──────────────────┘
               │
               ▼
┌─────────────────────────────────┐
│   Blueprint Handler             │
│   (e.g., books_bp.py)          │
└──────────────┬──────────────────┘
               │
               ▼
┌─────────────────────────────────┐
│   Route Function                │
│   (GET /api/books)              │
└──────────────┬──────────────────┘
               │
               ▼
┌─────────────────────────────────┐
│   Input Validation              │
│   (Marshmallow schema)          │
└──────────────┬──────────────────┘
               │
               ▼
┌─────────────────────────────────┐
│   Business Logic                │
│   (services/ or models/)        │
└──────────────┬──────────────────┘
               │
               ▼
┌─────────────────────────────────┐
│   Database Query                │
│   (SQLAlchemy models)           │
└──────────────┬──────────────────┘
               │
               ▼
┌─────────────────────────────────┐
│   PostgreSQL                    │
└──────────────┬──────────────────┘
               │
               ▼
┌─────────────────────────────────┐
│   Response Serialization        │
│   (Marshmallow schema)          │
└──────────────┬──────────────────┘
               │
               ▼
         JSON Response
```

### 7c. Recommended Backend Folder Structure (Simplified POC)

```
backend/
├── app.py                          # Application factory
├── config.py                       # Configuration management
├── requirements.txt                # Python dependencies (minimal)
├── Dockerfile                      # Docker configuration
├── .dockerignore                   # Docker ignore patterns
│
├── routes/                         # API endpoints (raw SQL queries)
│   ├── __init__.py
│   ├── books.py                    # Book endpoints (GET, POST, PUT, DELETE)
│   ├── book_status.py              # Reading status endpoints
│   ├── reviews.py                  # Review endpoints
│   ├── tbr.py                      # TBR list endpoints
│   └── stats.py                    # Statistics endpoints
│
├── db.py                           # Database connection helper
│   └── Database connection pooling (simple connection)
│
├── utils/                          # Helper functions
│   ├── __init__.py
│   ├── validators.py               # Basic input validation
│   └── constants.py                # Constants (status enums, etc.)
│
├── sql/                            # SQL schema and seed data
│   ├── schema.sql                  # CREATE TABLE statements
│   ├── seed.sql                    # Sample data for testing
│   └── queries.sql                 # Common SQL queries (reference)
│
├── tests/                          # Test suite
│   ├── __init__.py
│   ├── conftest.py                 # Pytest fixtures
│   ├── test_books.py               # Test book endpoints
│   ├── test_book_status.py         # Test reading status
│   ├── test_reviews.py             # Test review endpoints
│   └── fixtures/                   # Test data
│       └── sample_data.sql
│
└── logs/                           # Application logs (generated)
    └── .gitkeep
```

### 7d. Key Backend Patterns (Simple POC)

**Application Factory Pattern**
```python
# app.py
from flask import Flask
from routes import books_bp, reviews_bp, tbr_bp, stats_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Development')
    
    # Register blueprints
    app.register_blueprint(books_bp)
    app.register_blueprint(reviews_bp)
    app.register_blueprint(tbr_bp)
    app.register_blueprint(stats_bp)
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, port=5000)
```

**Database Connection Helper**
```python
# db.py
import psycopg2
import psycopg2.extras
import os

def get_db_connection():
    """Simple database connection"""
    return psycopg2.connect(
        host=os.getenv('DB_HOST', 'postgres'),
        database=os.getenv('DB_NAME', 'library_db'),
        user=os.getenv('DB_USER', 'postgres'),
        password=os.getenv('DB_PASSWORD', 'password'),
        port=os.getenv('DB_PORT', '5432')
    )

def dict_cursor():
    """Return a cursor that returns results as dictionaries"""
    return psycopg2.extras.RealDictCursor
```

**Blueprint with Raw SQL**
```python
# routes/books.py
from flask import Blueprint, request, jsonify
from db import get_db_connection, dict_cursor

books_bp = Blueprint('books', __name__, url_prefix='/api/books')

@books_bp.route('', methods=['GET'])
def list_books():
    """GET /api/books - List all books"""
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=dict_cursor())
    
    try:
        cur.execute('SELECT * FROM books ORDER BY title')
        books = cur.fetchall()
        return jsonify(books)
    finally:
        cur.close()
        conn.close()

@books_bp.route('/<int:book_id>', methods=['GET'])
def get_book(book_id):
    """GET /api/books/{id}"""
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=dict_cursor())
    
    try:
        cur.execute('SELECT * FROM books WHERE id = %s', (book_id,))
        book = cur.fetchone()
        return jsonify(book) if book else ({}, 404)
    finally:
        cur.close()
        conn.close()

@books_bp.route('', methods=['POST'])
def create_book():
    """POST /api/books - Create a new book"""
    data = request.json
    conn = get_db_connection()
    cur = conn.cursor()
    
    try:
        cur.execute("""
            INSERT INTO books (title, author_id, pages, genre, description, cover_url)
            VALUES (%s, %s, %s, %s, %s, %s)
            RETURNING id
        """, (data['title'], data['author_id'], data['pages'], 
              data.get('genre'), data.get('description'), data.get('cover_url')))
        
        new_id = cur.fetchone()[0]
        conn.commit()
        return {'id': new_id, 'message': 'Book created'}, 201
    except Exception as e:
        conn.rollback()
        return {'error': str(e)}, 400
    finally:
        cur.close()
        conn.close()
```

**Raw SQL Queries with psycopg2**
```python
# routes/books.py
import psycopg2
import psycopg2.extras

def get_db_connection():
    """Get database connection"""
    conn = psycopg2.connect(
        host=os.getenv('DB_HOST'),
        database=os.getenv('DB_NAME'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD')
    )
    return conn

@books_bp.route('', methods=['GET'])
def list_books():
    """GET /api/books - List all books with status"""
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    
    try:
        # Simple raw SQL query
        cur.execute("""
            SELECT b.*, bs.status, bs.rating, bs.is_tbr
            FROM books b
            LEFT JOIN book_status bs ON b.id = bs.book_id
            ORDER BY b.title
            LIMIT 50
        """)
        books = cur.fetchall()
        return jsonify(books)
    finally:
        cur.close()
        conn.close()

@books_bp.route('/<int:book_id>/status', methods=['PUT'])
def update_book_status(book_id):
    """PUT /api/books/{id}/status - Update reading status"""
    data = request.json
    conn = get_db_connection()
    cur = conn.cursor()
    
    try:
        # Parameterized query (prevents SQL injection)
        cur.execute("""
            UPDATE book_status 
            SET status = %s, 
                date_started = CASE WHEN %s = 'reading' THEN NOW() ELSE date_started END,
                date_completed = CASE WHEN %s = 'completed' THEN NOW() ELSE date_completed END
            WHERE book_id = %s
        """, (data['status'], data['status'], data['status'], book_id))
        
        conn.commit()
        return {'status': 'updated'}, 200
    finally:
        cur.close()
        conn.close()
```

## 8. Technology Stack

### Backend (POC - Simple & Direct)
- **Framework**: Flask (lightweight, minimal setup)
- **Database**: PostgreSQL 14+ (raw SQL queries via `psycopg2`)
- **No ORM**: Direct SQL execution (simpler for POC)
- **No Auth**: Single-user, no authentication needed
- **Validation**: Basic Python validation (keep it simple)
- **Testing**: pytest

### Frontend
- **Framework**: React 18+
- **State Management**: Context API or Zustand
- **HTTP Client**: Axios or Fetch
- **UI Library**: Tailwind CSS (lightweight) or Material-UI
- **Routing**: React Router
- **Build Tool**: Vite

### Infrastructure
- **Container Runtime**: Docker
- **Orchestration**: Docker Compose (local only)
- **Database**: PostgreSQL 14+
- **Environment**: Python 3.11+, Node.js 18+

## 10. Future Extensibility Considerations

### Recommendation System
- Collaborative filtering (user-user similarity)
- Content-based filtering (genre/author similarity)
- Hybrid approach combining both
- Integration with reading preferences stored in database

### Reading Completion Prediction
- Track reading sessions with dates and pages read
- Use time-series analysis to predict completion
- Consider book difficulty (pages) and user reading speed
- ML model trained on historical reading patterns

### Additional Features
- Social features (friend lists, shared reviews)
- Reading challenges (yearly goals, category challenges)
- Importing from Goodreads
- Book club features (group reading, discussions)
- Email notifications (recommendation digests, reading reminders)
- Mobile app (React Native or Flutter)

## 11. Important Notes (POC Only)

⚠️ **This is a Proof of Concept, not production-ready:**
- No authentication or authorization
- No password hashing or security measures
- Single-user only (local development)
- Basic input validation only
- No HTTPS, no CORS protection
- Not suitable for production or sensitive data

**If converting to production later, add:**
- Input validation and sanitization
- Parameterized SQL queries (already doing with psycopg2)
- Authentication system
- HTTPS/SSL
- Rate limiting
- Logging and monitoring

## 12. Development Environment Setup

### Docker Compose Services
```yaml
services:
  postgres:
    image: postgres:16-alpine
    ports: 5432:5432
    volumes: [data]
    env: [db_password, db_name]
    
  backend:
    build: ./backend
    ports: 5000:5000
    depends_on: [postgres]
    volumes: [source code for hot reload]
    env: [db_connection, debug_mode]
    
  frontend:
    build: ./frontend
    ports: 3000:3000
    depends_on: [backend]
    volumes: [source code for hot reload]
    env: [api_url, environment]
```

## 13. Testing Strategy

### Backend
- Unit tests for business logic
- Integration tests for API endpoints
- Database fixtures with test data
- Test coverage target: 80%+

### Frontend
- Component tests with React Testing Library
- Integration tests for user flows
- Mock API responses
- Test coverage target: 70%+

### E2E
- Selenium or Playwright for user journey testing
- Test core workflows: add book, mark as read, write review, view TBR

## 14. Deployment Strategy

### Local Development
- Docker Compose for full stack
- Hot reload for code changes
- Seed database with sample data

### Production (Future)
- Docker images to registry (Docker Hub / ECR)
- Kubernetes deployment with Helm charts
- CI/CD pipeline (GitHub Actions)
- Database migrations via Alembic
- Environment-specific configurations

## 15. Performance Considerations

- Pagination for book listings (20-50 items per page)
- Caching user's own books in frontend state
- Database indexing on frequently queried columns (user_id, status)
- API response compression (gzip)
- Lazy loading for book covers/images
- Connection pooling for database

## 16. Monitoring & Logging

- Application logs (structured logging with timestamps)
- Database query logging (in dev, selectively in prod)
- API performance metrics
- Error tracking (Sentry integration - future)
- User analytics (optional - future)
