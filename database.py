import sqlite3
import json
import threading
import os

# Thread-local storage for connections (har bir thread o'z connectioni bilan ishlaydi)
_local = threading.local()

# Absolute path — bot qayerdan ishga tushirilsa ham to'g'ri ishlaydi
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, 'bot_database.db')

def get_conn():
    """Har bir thread uchun alohida connection qaytaradi."""
    if not hasattr(_local, 'conn') or _local.conn is None:
        _local.conn = sqlite3.connect(DB_PATH, check_same_thread=False, timeout=10)
        _local.conn.execute("PRAGMA journal_mode=WAL")  # Ko'p foydalanuvchi uchun
        _local.conn.execute("PRAGMA synchronous=NORMAL")
    return _local.conn

def init_db():
    conn = sqlite3.connect(DB_PATH, timeout=10)
    conn.execute("PRAGMA journal_mode=WAL")
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            telegram_id INTEGER UNIQUE,
            default_lang TEXT DEFAULT 'uz',
            correct_answers INTEGER DEFAULT 0,
            total_questions INTEGER DEFAULT 0
        )
    ''')

    try:
        cursor.execute("ALTER TABLE users ADD COLUMN correct_answers INTEGER DEFAULT 0")
        cursor.execute("ALTER TABLE users ADD COLUMN total_questions INTEGER DEFAULT 0")
        conn.commit()
    except sqlite3.OperationalError:
        pass

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS words (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            category TEXT,
            qq TEXT,
            uz TEXT,
            example_qq TEXT,
            example_uz TEXT,
            photo_id TEXT,
            voice_id TEXT
        )
    ''')

    cursor.execute('SELECT COUNT(*) FROM words')
    if cursor.fetchone()[0] == 0:
        with open('data.json', 'r', encoding='utf-8') as f:
            data = json.load(f)

        sample_words = []
        for category, words in data.items():
            for w in words:
                sample_words.append((
                    category,
                    w['qq'],
                    w['uz'],
                    w.get('example_qq', ''),
                    w.get('example_uz', ''),
                    None,
                    None
                ))

        cursor.executemany('''
            INSERT INTO words (category, qq, uz, example_qq, example_uz, photo_id, voice_id)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', sample_words)

    conn.commit()
    conn.close()


def add_user(telegram_id):
    conn = sqlite3.connect(DB_PATH, timeout=10)
    conn.execute("PRAGMA journal_mode=WAL")
    cursor = conn.cursor()
    is_new = False
    try:
        cursor.execute('INSERT INTO users (telegram_id) VALUES (?)', (telegram_id,))
        conn.commit()
        is_new = True
    except sqlite3.IntegrityError:
        pass
    conn.close()
    return is_new


def set_user_language(telegram_id, lang):
    conn = sqlite3.connect(DB_PATH, timeout=10)
    conn.execute("PRAGMA journal_mode=WAL")
    cursor = conn.cursor()
    try:
        cursor.execute(
            'UPDATE users SET default_lang = ? WHERE telegram_id = ?',
            (lang, telegram_id)
        )
        conn.commit()
    except sqlite3.Error as e:
        print(f"Database error: {e}")
    conn.close()


def get_user_language(telegram_id):
    conn = sqlite3.connect(DB_PATH, timeout=10)
    conn.execute("PRAGMA journal_mode=WAL")
    cursor = conn.cursor()
    cursor.execute('SELECT default_lang FROM users WHERE telegram_id = ?', (telegram_id,))
    result = cursor.fetchone()
    conn.close()
    return result[0] if result else 'uz'


def update_user_stats(telegram_id, is_correct):
    conn = sqlite3.connect(DB_PATH, timeout=10)
    conn.execute("PRAGMA journal_mode=WAL")
    cursor = conn.cursor()
    if is_correct:
        cursor.execute(
            'UPDATE users SET correct_answers = correct_answers + 1, total_questions = total_questions + 1 WHERE telegram_id = ?',
            (telegram_id,)
        )
    else:
        cursor.execute(
            'UPDATE users SET total_questions = total_questions + 1 WHERE telegram_id = ?',
            (telegram_id,)
        )
    conn.commit()
    conn.close()


def update_bulk_user_stats(telegram_id, correct_count, total_count):
    conn = sqlite3.connect(DB_PATH, timeout=10)
    conn.execute("PRAGMA journal_mode=WAL")
    cursor = conn.cursor()
    cursor.execute(
        'UPDATE users SET correct_answers = correct_answers + ?, total_questions = total_questions + ? WHERE telegram_id = ?',
        (correct_count, total_count, telegram_id)
    )
    conn.commit()
    conn.close()


def get_user_stats(telegram_id):
    conn = sqlite3.connect(DB_PATH, timeout=10)
    conn.execute("PRAGMA journal_mode=WAL")
    cursor = conn.cursor()
    cursor.execute(
        'SELECT correct_answers, total_questions FROM users WHERE telegram_id = ?',
        (telegram_id,)
    )
    result = cursor.fetchone()
    conn.close()
    return result if result else (0, 0)


def get_word(category, index):
    conn = sqlite3.connect(DB_PATH, timeout=10)
    conn.execute("PRAGMA journal_mode=WAL")
    cursor = conn.cursor()
    cursor.execute(
        'SELECT * FROM words WHERE category = ? LIMIT 1 OFFSET ?',
        (category, index)
    )
    word = cursor.fetchone()
    conn.close()
    return word


def get_words_count(category):
    conn = sqlite3.connect(DB_PATH, timeout=10)
    conn.execute("PRAGMA journal_mode=WAL")
    cursor = conn.cursor()
    cursor.execute('SELECT COUNT(*) FROM words WHERE category = ?', (category,))
    count = cursor.fetchone()[0]
    conn.close()
    return count


def get_random_words(limit=4):
    conn = sqlite3.connect(DB_PATH, timeout=10)
    conn.execute("PRAGMA journal_mode=WAL")
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM words ORDER BY RANDOM() LIMIT ?', (limit,))
    words = cursor.fetchall()
    conn.close()
    return words


def get_picture_dictionary_words(limit_per_category=2):
    conn = sqlite3.connect(DB_PATH, timeout=10)
    conn.execute("PRAGMA journal_mode=WAL")
    cursor = conn.cursor()
    categories = [
        'salemlesiw', 'kundelikli', 'waqit', 'shanaraq', 'sanlar',
        'aziq_awqat', 'renler', 'tabiyaat', 'oqiw', 'kiyimler',
        'janiwarlar', 'miyweler', 'oyinshiqlar', 'dene_agzalari'
    ]
    result = []
    for cat in categories:
        cursor.execute(
            'SELECT id, category, qq, uz FROM words WHERE category = ? LIMIT ?',
            (cat, limit_per_category)
        )
        result.extend(cursor.fetchall())
    conn.close()
    return result


def get_word_by_id(word_id):
    conn = sqlite3.connect(DB_PATH, timeout=10)
    conn.execute("PRAGMA journal_mode=WAL")
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM words WHERE id = ?', (word_id,))
    word = cursor.fetchone()
    conn.close()
    return word
