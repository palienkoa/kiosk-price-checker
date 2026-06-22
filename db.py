"""Шар доступу до SQLite: ініціалізація, upsert, пошук за штрихкодом."""
import sqlite3
from datetime import datetime
from pathlib import Path

# Папка data/ поруч із цим файлом; там лежить файл бази.
BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "data" / "catalog.db"
SCHEMA_PATH = BASE_DIR / "schema.sql"


def get_connection():
    """Відкриває з'єднання з базою. row_factory=Row дає доступ до полів за іменем."""
    DB_PATH.parent.mkdir(exist_ok=True)  # створити папку data/, якщо її ще нема
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """Створює таблицю за schema.sql (безпечно запускати багато разів)."""
    schema_sql = SCHEMA_PATH.read_text(encoding="utf-8")
    with get_connection() as conn:
        conn.executescript(schema_sql)


def upsert_product(barcode, name, price, qty, picture_path=None, changed_at=None):
    """Вставити товар або оновити, якщо штрихкод уже є (INSERT ... ON CONFLICT)."""
    now = datetime.now().isoformat(timespec="seconds")
    with get_connection() as conn:
        conn.execute(
            """
            INSERT INTO products (barcode, name, price, qty, picture_path, changed_at, synced_at)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(barcode) DO UPDATE SET
                name         = excluded.name,
                price        = excluded.price,
                qty          = excluded.qty,
                picture_path = excluded.picture_path,
                changed_at   = excluded.changed_at,
                synced_at    = excluded.synced_at
            """,
            (barcode, name, price, qty, picture_path, changed_at, now),
        )


def get_by_barcode(barcode):
    """Повертає один рядок товару (sqlite3.Row) або None, якщо не знайдено."""
    with get_connection() as conn:
        cur = conn.execute("SELECT * FROM products WHERE barcode = ?", (barcode,))
        return cur.fetchone()
