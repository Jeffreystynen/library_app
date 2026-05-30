-- Library App Seed Data
-- REAL LITERARY CLASSICS with fictional reading history (POC)
-- 25+ books across 5 genres

-- Authors (Real Literary Classics)
INSERT INTO authors (name, biography, country, website_url) VALUES
('Jane Austen', 'English novelist known for her romantic fiction and social commentary. Pioneer of the novel of manners.', 'United Kingdom', NULL),
('George Orwell', 'British writer and journalist famous for dystopian novels exploring politics and totalitarianism.', 'United Kingdom', NULL),
('F. Scott Fitzgerald', 'American novelist capturing the decadence of the Jazz Age with elegant prose.', 'United States', NULL),
('Fyodor Dostoevsky', 'Russian novelist exploring themes of morality, faith, and human psychology.', 'Russia', NULL),
('Jane Eyre (Charlotte Brontë)', 'English novelist known for Gothic romantic fiction and strong female protagonists.', 'United Kingdom', NULL),
('Leo Tolstoy', 'Russian novelist master of epic narratives about Russian society and human condition.', 'Russia', NULL),
('Jules Verne', 'French author pioneer of science fiction exploring technological possibilities.', 'France', NULL),
('Mary Shelley', 'English novelist author of the first modern science fiction novel.', 'United Kingdom', NULL),
('Agatha Christie', 'British mystery writer creating intricate detective narratives.', 'United Kingdom', NULL),
('Emily Brontë', 'English novelist known for her passionate romantic fiction.', 'United Kingdom', NULL),
('Charles Dickens', 'English novelist chronicling Victorian society with vivid characters.', 'United Kingdom', NULL),
('Emily Dickinson', 'American poet exploring themes of mortality and identity.', 'United States', NULL),
('Oscar Wilde', 'Irish playwright and novelist known for witty social comedies.', 'Ireland', NULL),
('Robert Louis Stevenson', 'Scottish novelist and poet author of adventure classics and gothic tales.', 'United Kingdom', NULL),
('Haruki Murakami', 'Japanese novelist blending magical realism with contemporary life.', 'Japan', NULL),
('Gabriel García Márquez', 'Colombian novelist master of magical realism and lyrical prose.', 'Colombia', NULL);

-- Books (Real Literary Classics - 26 books across 5 genres)
INSERT INTO books (isbn, title, author_id, publication_year, genre, description, pages) VALUES
-- LITERARY FICTION/CLASSICS (7 books)
('978-0141439600', 'Pride and Prejudice', 1, 1813, ARRAY['Literary Fiction', 'Romance', 'Classic'], 'Elizabeth Bennet navigates societal expectations and personal desires in Georgian England.', 279),
('978-0451524935', 'Crime and Punishment', 4, 1866, ARRAY['Literary Fiction', 'Psychological', 'Classic'], 'A young student commits murder and struggles with guilt and redemption in St. Petersburg.', 671),
('978-0140439655', 'Jane Eyre', 5, 1847, ARRAY['Literary Fiction', 'Gothic', 'Classic'], 'An orphan girl finds love and independence despite a tragic past.', 448),
('978-0199232765', 'Anna Karenina', 6, 1877, ARRAY['Literary Fiction', 'Drama', 'Classic'], 'Tolstoy''s epic novel exploring love, family, and Russian society across generations.', 964),
('978-0141182667', 'Wuthering Heights', 10, 1847, ARRAY['Literary Fiction', 'Gothic', 'Classic'], 'A passionate and destructive love story set on the Yorkshire moors.', 323),
('978-0451531292', 'The Brothers Karamazov', 4, 1879, ARRAY['Literary Fiction', 'Philosophical', 'Classic'], 'Four brothers confronting faith, morality, and family legacy in Russia.', 976),
('978-0451532206', 'Dickens: Great Expectations', 11, 1861, ARRAY['Literary Fiction', 'Drama', 'Classic'], 'Pip''s journey from humble beginnings to gentleman reveals the true meaning of expectations.', 505),

-- SCIENCE FICTION/FANTASY (7 books)
('978-0451524934', 'Frankenstein', 8, 1818, ARRAY['Science Fiction', 'Gothic', 'Classic'], 'Victor Frankenstein''s creation of life leads to obsession and tragedy.', 280),
('978-0451526342', 'Twenty Thousand Leagues Under the Sea', 7, 1870, ARRAY['Science Fiction', 'Adventure', 'Classic'], 'Captain Nemo''s extraordinary submarine voyage exploring the ocean depths.', 488),
('978-0451525871', 'The Time Machine', 7, 1895, ARRAY['Science Fiction', 'Classic'], 'An inventor travels through time witnessing humanity''s distant future.', 109),
('978-0141442778', '1984', 2, 1949, ARRAY['Science Fiction', 'Dystopian', 'Classic'], 'A totalitarian state controls every aspect of citizens'' lives in this chilling dystopia.', 328),
('978-0141391823', 'The Lord of the Rings', 7, 1954, ARRAY['Fantasy', 'Epic', 'Classic'], 'A hobbit''s epic quest to destroy a ring of power and save Middle-earth.', 1146),
('978-0451453532', 'Brave New World', 2, 1932, ARRAY['Science Fiction', 'Dystopian', 'Classic'], 'A future society achieves stability through pleasure and control in this cautionary tale.', 311),
('978-0141192246', 'The Hobbit', 7, 1937, ARRAY['Fantasy', 'Adventure', 'Classic'], 'Bilbo Baggins embarks on an unexpected journey with dwarves and a wizard.', 310),

-- MYSTERY/THRILLER (6 books)
('978-0451463265', 'Murder on the Orient Express', 9, 1934, ARRAY['Mystery', 'Detective', 'Classic'], 'Detective Poirot solves a locked-room murder on a snowbound train.', 256),
('978-0062073556', 'The Girl on the Train', 9, 1939, ARRAY['Mystery', 'Thriller'], 'An amateur detective uncovers secrets on her daily commute.', 309),
('978-0451465016', 'And Then There Were None', 9, 1939, ARRAY['Mystery', 'Thriller', 'Classic'], 'Ten strangers invited to an island are eliminated one by one in this locked-room mystery.', 272),
('978-0451525406', 'The Moonstone', 11, 1868, ARRAY['Mystery', 'Detective', 'Classic'], 'Often considered the first detective novel, featuring the theft of a valuable diamond.', 464),
('978-0451529800', 'The Hound of the Baskervilles', 2, 1901, ARRAY['Mystery', 'Detective', 'Classic'], 'Sherlock Holmes investigates a legendary curse threatening the Baskerville family.', 256),
('978-0141192283', 'The Strange Case of Dr. Jekyll and Mr. Hyde', 2, 1886, ARRAY['Mystery', 'Psychological', 'Classic'], 'A scientist''s experiment transforms him into an evil alter ego in this Gothic tale.', 96),

-- ROMANCE (4 books)
('978-0141439570', 'Sense and Sensibility', 1, 1811, ARRAY['Romance', 'Literary', 'Classic'], 'Two sisters with different temperaments navigate love and marriage in Regency England.', 409),
('978-0140436846', 'The Great Gatsby', 3, 1925, ARRAY['Romance', 'Literary', 'Classic'], 'Gatsby''s obsessive love for Daisy defines the American Dream in the Jazz Age.', 180),
('978-0451527272', 'Emily Dickinson: Selected Poems', 12, 1890, ARRAY['Romance', 'Poetry', 'Classic'], 'Intimate and innovative verses exploring love, mortality, and existence.', 224),
('978-0451531018', 'Persuasion', 1, 1817, ARRAY['Romance', 'Literary', 'Classic'], 'Anne Elliot''s second chance at love with Captain Wentworth after years of separation.', 271),

-- ADVENTURE/DRAMA (2 books)
('978-0451525345', 'Robinson Crusoe', 11, 1719, ARRAY['Adventure', 'Survival', 'Classic'], 'A man survives shipwreck and builds a life on a remote island for 28 years.', 368),
('978-0451526785', 'Treasure Island', 14, 1882, ARRAY['Adventure', 'Pirate', 'Classic'], 'A boy joins pirates searching for buried treasure on a mysterious island.', 320);

-- Book Status (mix of different reading states and ratings for 26 books)
INSERT INTO book_status (book_id, status, date_added, date_started, date_completed, rating, is_tbr, notes, pages_read) VALUES
(1, 'completed', '2026-01-15', '2026-01-16', '2026-02-02', 5, FALSE, 'Austen''s wit and social commentary are timeless. Elizabeth is iconic!', 279),
(2, 'completed', '2026-01-10', '2026-01-12', '2026-03-01', 4, FALSE, 'Dense but brilliant. The psychology of Raskolnikov is mesmerizing.', 671),
(3, 'completed', '2025-12-15', '2025-12-17', '2026-01-20', 5, FALSE, 'Gothic masterpiece. Jane Eyre remains one of my favorites.', 448),
(4, 'completed', '2026-02-01', '2026-02-03', '2026-03-25', 4, FALSE, 'Tolstoy at his finest. Epic in scope but deeply personal.', 964),
(5, 'completed', '2026-01-20', '2026-01-22', '2026-02-15', 4, FALSE, 'Passionate and dark. Emily Brontë''s only novel is haunting.', 323),
(6, 'reading', '2026-04-20', '2026-04-21', NULL, NULL, FALSE, 'Currently on page 412. Dostoevsky explores faith and morality brilliantly.', 412),
(7, 'reading', '2026-04-25', '2026-04-26', NULL, NULL, FALSE, 'Page 278. Dickens'' vivid characters bring Victorian England to life.', 278),
(8, 'completed', '2026-01-05', '2026-01-07', '2026-01-25', 5, FALSE, 'The original science fiction novel. Still captivating and terrifying.', 280),
(9, 'completed', '2025-12-01', '2025-12-05', '2026-01-10', 5, FALSE, 'Verne''s imagination knows no bounds. An adventure classic.', 488),
(10, 'completed', '2026-01-08', '2026-01-09', '2026-01-20', 4, FALSE, 'Brilliant time travel story. Simple but profound.', 109),
(11, 'completed', '2026-02-10', '2026-02-12', '2026-03-20', 5, FALSE, '1984 is more relevant than ever. A chilling masterpiece.', 328),
(12, 'tbr', '2026-05-01', NULL, NULL, NULL, TRUE, 'Can''t wait to read this epic fantasy. Building up to it.', 0),
(13, 'unread', '2026-04-28', NULL, NULL, NULL, FALSE, 'Huxley''s classic dystopia. Added to library, ready to read when I get to it.', 0),
(14, 'tbr', '2026-05-05', NULL, NULL, NULL, TRUE, 'A classic adventure. On my priority list.', 0),
(15, 'completed', '2026-01-25', '2026-01-27', '2026-02-20', 4, FALSE, 'Murder on a train. Christie at her best with Poirot.', 256),
(16, 'unread', '2026-05-02', NULL, NULL, NULL, FALSE, 'Modern mystery with unreliable narrators. Curious to see how it compares to classics.', 0),
(17, 'completed', '2026-01-30', '2026-02-01', '2026-02-18', 5, FALSE, 'Ten strangers, ten murders. A masterpiece of suspense.', 272),
(18, 'tbr', '2026-05-08', NULL, NULL, NULL, TRUE, 'The first detective novel ever written. Historical importance.', 0),
(19, 'unread', '2026-04-15', NULL, NULL, NULL, FALSE, 'Sherlock Holmes classic. Interested in revisiting the detective stories.', 0),
(20, 'completed', '2026-01-12', '2026-01-14', '2026-01-25', 4, FALSE, 'Jekyll and Hyde is Gothic perfection. Still disturbing.', 96),
(21, 'completed', '2026-02-05', '2026-02-07', '2026-02-25', 4, FALSE, 'Austen''s sense and sensibility balance in two sisters.', 409),
(22, 'completed', '2026-01-03', '2026-01-05', '2026-01-30', 5, FALSE, 'Fitzgerald captures the Jazz Age and the American Dream perfectly.', 180),
(23, 'tbr', '2026-05-10', NULL, NULL, NULL, TRUE, 'Emily Dickinson''s incredible poetry. Ready to be moved.', 0),
(24, 'unread', '2026-04-28', NULL, NULL, NULL, FALSE, 'Austen''s final novel. Want to read all her works eventually.', 0),
(25, 'unread', '2026-05-08', NULL, NULL, NULL, FALSE, 'A survival classic. Haven''t gotten to it yet.', 0),
(26, 'tbr', '2026-05-12', NULL, NULL, NULL, TRUE, 'Pirate adventure with treasure and mystery.', 0);

-- Reviews (for completed classic books)
INSERT INTO reviews (book_id, rating, title, content, spoiler_warning) VALUES
(1, 5, 'Timeless Masterpiece', 'Pride and Prejudice remains as witty and charming as ever. Austen''s social commentary is sharp, the romance between Elizabeth and Darcy is perfectly paced, and the side characters are hilarious. A book that rewards rereading.', FALSE),
(2, 4, 'Dense but Brilliant', 'Crime and Punishment is not an easy read, but it''s profoundly rewarding. Dostoevsky''s exploration of guilt, morality, and redemption through Raskolnikov''s psychology is unmatched. The philosophical depth will stay with you long after finishing.', FALSE),
(3, 5, 'Gothic Perfection', 'Jane Eyre is one of the greatest novels in English literature. Charlotte Brontë creates an unforgettable protagonist in Jane, and the Gothic atmosphere is perfectly maintained throughout. The romance feels earned and genuine.', FALSE),
(4, 4, 'Epic Scope and Intimacy', 'Anna Karenina is Tolstoy at his absolute finest. The parallel stories of Anna and Levin explore love, society, and the meaning of life in ways that still feel modern. At nearly 1000 pages, it earns every word.', FALSE),
(5, 4, 'Passion and Darkness', 'Wuthering Heights is raw, passionate, and utterly compelling. Emily Brontë''s only novel remains one of the greatest love stories ever written, but it''s also a tale of revenge and damage that lingers in the mind.', FALSE),
(8, 5, 'The First Science Fiction Novel', 'Frankenstein is absolutely brilliant. Mary Shelley created the template for science fiction while also writing a deeply philosophical novel about creation, responsibility, and what it means to be human. Timeless.', FALSE),
(9, 5, 'Adventure Without Peer', 'Twenty Thousand Leagues Under the Sea captures the imagination like nothing else. Verne''s descriptions of the ocean depths and the Nautilus are vivid and thrilling. Captain Nemo is one of literature''s great characters.', FALSE),
(10, 4, 'Brilliantly Simple', 'The Time Machine is short but packed with ideas. Wells uses time travel to explore society, evolution, and human nature. It''s a philosophical thriller that entertains while making you think.', FALSE),
(11, 5, '1984 Remains Chilling', 'Orwell''s vision of totalitarianism is more prescient than ever. The surveillance state, propaganda, and psychological control he describes feel frighteningly close to modern reality. A must-read that will disturb and enlighten.', FALSE),
(15, 5, 'Murder on a Train Perfected', 'Murder on the Orient Express is Christie at her absolute best. The locked-room mystery, the parade of suspects, and the brilliant solution make this one of the greatest detective stories ever written.', FALSE),
(17, 5, 'Masterpiece of Suspense', 'And Then There Were None is possibly the perfect mystery novel. Ten strangers, a mysterious host, and a nursery rhyme predicting murders. The tension builds brilliantly to an unforgettable ending.', FALSE),
(20, 4, 'Gothic Horror Classic', 'The Strange Case of Dr. Jekyll and Mr. Hyde is brief but incredibly impactful. Stevenson''s exploration of the duality of human nature and the suppressed darkness within us all is as relevant today as in 1886.', FALSE),
(21, 4, 'Austen''s Subtle Brilliance', 'Sense and Sensibility showcases Austen''s wit as she explores two sisters with opposite temperaments. The plot is charming, the romance is satisfying, and the social commentary on women''s options is both funny and sad.', FALSE),
(22, 5, 'The Great American Novel', 'The Great Gatsby is a short masterpiece that captures an era and tells a deeply tragic love story. Fitzgerald''s prose is beautiful, Gatsby is unforgettable, and the ending is devastating. A classic for good reason.', FALSE);

-- Reading Sessions (for ML model training - fictional but realistic patterns)
-- Pride and Prejudice (279 pages, completed in 18 days)
INSERT INTO reading_sessions (book_id, session_date, pages_read, duration_minutes) VALUES
(1, '2026-01-16', 35, 70),
(1, '2026-01-17', 42, 85),
(1, '2026-01-18', 38, 75),
(1, '2026-01-20', 44, 90),
(1, '2026-01-21', 40, 80),
(1, '2026-01-22', 45, 90),
(1, '2026-01-23', 35, 70);

-- Crime and Punishment (671 pages, completed in 58 days - dense book, slower pace)
INSERT INTO reading_sessions (book_id, session_date, pages_read, duration_minutes) VALUES
(2, '2026-01-12', 28, 75),
(2, '2026-01-14', 32, 85),
(2, '2026-01-16', 25, 70),
(2, '2026-01-18', 35, 90),
(2, '2026-01-21', 30, 80),
(2, '2026-01-23', 28, 75),
(2, '2026-01-25', 33, 85),
(2, '2026-01-27', 26, 70),
(2, '2026-01-29', 31, 80),
(2, '2026-02-01', 29, 75),
(2, '2026-02-03', 34, 85),
(2, '2026-02-05', 27, 70);

-- Jane Eyre (448 pages, completed in 32 days)
INSERT INTO reading_sessions (book_id, session_date, pages_read, duration_minutes) VALUES
(3, '2025-12-17', 45, 90),
(3, '2025-12-19', 48, 95),
(3, '2025-12-21', 42, 85),
(3, '2025-12-23', 50, 100),
(3, '2025-12-25', 44, 90),
(3, '2025-12-27', 46, 95),
(3, '2025-12-29', 41, 85),
(3, '2026-01-02', 47, 95),
(3, '2026-01-04', 43, 90),
(3, '2026-01-06', 49, 100),
(3, '2026-01-08', 45, 95),
(3, '2026-01-10', 48, 100),
(3, '2026-01-12', 0, 0);

-- Anna Karenina (964 pages, completed in 80 days - epic, multiple reading sessions)
INSERT INTO reading_sessions (book_id, session_date, pages_read, duration_minutes) VALUES
(4, '2026-02-03', 32, 85),
(4, '2026-02-05', 35, 90),
(4, '2026-02-07', 28, 75),
(4, '2026-02-09', 38, 95),
(4, '2026-02-11', 30, 80),
(4, '2026-02-13', 33, 85),
(4, '2026-02-15', 36, 90),
(4, '2026-02-17', 29, 75),
(4, '2026-02-19', 34, 85),
(4, '2026-02-21', 37, 95),
(4, '2026-02-23', 31, 80),
(4, '2026-02-25', 35, 90),
(4, '2026-02-27', 28, 75),
(4, '2026-03-01', 39, 100),
(4, '2026-03-03', 32, 85),
(4, '2026-03-05', 36, 90),
(4, '2026-03-07', 30, 80),
(4, '2026-03-09', 38, 95),
(4, '2026-03-11', 33, 85),
(4, '2026-03-13', 37, 95);

-- Wuthering Heights (323 pages, completed in 25 days)
INSERT INTO reading_sessions (book_id, session_date, pages_read, duration_minutes) VALUES
(5, '2026-01-22', 52, 105),
(5, '2026-01-24', 48, 95),
(5, '2026-01-26', 55, 110),
(5, '2026-01-28', 51, 100),
(5, '2026-01-30', 49, 100),
(5, '2026-02-01', 53, 105),
(5, '2026-02-03', 15, 30);

-- The Great Gatsby (180 pages, completed in 8 days - quick read)
INSERT INTO reading_sessions (book_id, session_date, pages_read, duration_minutes) VALUES
(22, '2026-01-05', 65, 110),
(22, '2026-01-06', 58, 100),
(22, '2026-01-07', 57, 100);

-- Frankenstein (280 pages, completed in 18 days)
INSERT INTO reading_sessions (book_id, session_date, pages_read, duration_minutes) VALUES
(8, '2026-01-07', 48, 95),
(8, '2026-01-09', 45, 90),
(8, '2026-01-11', 52, 105),
(8, '2026-01-13', 46, 92),
(8, '2026-01-15', 50, 100),
(8, '2026-01-17', 44, 88),
(8, '2026-01-19', 15, 30);

-- Twenty Thousand Leagues Under the Sea (488 pages, completed in 35 days)
INSERT INTO reading_sessions (book_id, session_date, pages_read, duration_minutes) VALUES
(9, '2025-12-05', 48, 95),
(9, '2025-12-07', 52, 105),
(9, '2025-12-09', 45, 90),
(9, '2025-12-11', 50, 100),
(9, '2025-12-13', 46, 95),
(9, '2025-12-15', 48, 98),
(9, '2025-12-17', 43, 88),
(9, '2025-12-19', 49, 100),
(9, '2025-12-21', 44, 90),
(9, '2025-12-23', 51, 102),
(9, '2026-01-02', 47, 95),
(9, '2026-01-04', 45, 92),
(9, '2026-01-06', 0, 0);

-- 1984 (328 pages, completed in 37 days)
INSERT INTO reading_sessions (book_id, session_date, pages_read, duration_minutes) VALUES
(11, '2026-02-12', 52, 105),
(11, '2026-02-14', 48, 95),
(11, '2026-02-16', 55, 110),
(11, '2026-02-18', 50, 100),
(11, '2026-02-20', 49, 100),
(11, '2026-02-22', 51, 105),
(11, '2026-02-24', 23, 45);

-- Murder on the Orient Express (256 pages, completed in 16 days)
INSERT INTO reading_sessions (book_id, session_date, pages_read, duration_minutes) VALUES
(15, '2026-02-01', 58, 110),
(15, '2026-02-03', 62, 120),
(15, '2026-02-05', 54, 105),
(15, '2026-02-07', 55, 110),
(15, '2026-02-09', 27, 55);

-- And Then There Were None (272 pages, completed in 18 days)
INSERT INTO reading_sessions (book_id, session_date, pages_read, duration_minutes) VALUES
(17, '2026-02-01', 65, 120),
(17, '2026-02-02', 58, 110),
(17, '2026-02-03', 60, 115),
(17, '2026-02-04', 52, 100),
(17, '2026-02-05', 37, 70);

-- Recent Reading Sessions for Currently Reading Books (April-May 2026 - active reading!)
-- The Brothers Karamazov (book 6) - good consistent pace
INSERT INTO reading_sessions (book_id, session_date, pages_read, duration_minutes) VALUES
(6, '2026-04-21', 25, 50),
(6, '2026-04-23', 28, 55),
(6, '2026-04-25', 32, 65),
(6, '2026-04-27', 30, 60),
(6, '2026-04-29', 35, 70),
(6, '2026-05-02', 33, 65),
(6, '2026-05-04', 36, 72),
(6, '2026-05-06', 31, 62),
(6, '2026-05-08', 38, 75),
(6, '2026-05-10', 34, 68),
(6, '2026-05-12', 37, 74),
(6, '2026-05-14', 29, 58),
(6, '2026-05-16', 40, 80),
(6, '2026-05-18', 35, 70),
(6, '2026-05-20', 42, 84),
(6, '2026-05-22', 39, 78),
(6, '2026-05-24', 41, 82),
(6, '2026-05-26', 38, 76),
(6, '2026-05-28', 43, 86);

-- Great Expectations (book 7) - steady reading pace
INSERT INTO reading_sessions (book_id, session_date, pages_read, duration_minutes) VALUES
(7, '2026-04-26', 18, 45),
(7, '2026-04-28', 20, 50),
(7, '2026-04-30', 22, 55),
(7, '2026-05-03', 25, 60),
(7, '2026-05-05', 19, 48),
(7, '2026-05-07', 24, 58),
(7, '2026-05-09', 26, 62),
(7, '2026-05-11', 21, 52),
(7, '2026-05-13', 27, 65),
(7, '2026-05-15', 23, 56),
(7, '2026-05-17', 29, 70),
(7, '2026-05-19', 20, 50),
(7, '2026-05-21', 28, 68),
(7, '2026-05-23', 25, 60),
(7, '2026-05-25', 30, 72),
(7, '2026-05-27', 26, 62);

-- TBR List
INSERT INTO tbr_list (name, description) VALUES
('My Reading List', 'Books I want to read next, prioritized');

-- TBR Items (books marked as TBR in book_status - good mix for demo)
INSERT INTO tbr_items (tbr_list_id, book_id, priority) VALUES
(1, 12, 1),  -- The Lord of the Rings - Epic fantasy, high priority
(1, 26, 2),  -- Treasure Island - Adventure, good lighter read
(1, 18, 3),  -- The Moonstone - Mystery/detective novel
(1, 14, 4),  -- The Hobbit - Fantasy, classic series
(1, 23, 5);  -- Emily Dickinson Selected Poems - Poetry, shorter

-- Preferences/Settings
INSERT INTO preferences (key, value) VALUES
('theme', 'light'),
('yearly_reading_goal', '24'),
('favorite_genres', 'Thriller,Science Fiction,Romance'),
('last_updated', CURRENT_TIMESTAMP::TEXT);
