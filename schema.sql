-- Таблиця товарів кіоска. Дані read-only, наповнюються синхрою з 1С (поки що seed-ом).
CREATE TABLE IF NOT EXISTS products (
    barcode      TEXT PRIMARY KEY,   -- штрихкод = ключ пошуку (як код довідника)
    name         TEXT NOT NULL,      -- назва товару
    price        REAL,               -- ціна
    qty          REAL,               -- залишок
    picture_path TEXT,               -- шлях до картинки в static/images або NULL
    changed_at   TEXT,               -- мітка зміни з 1С (для інкрементальної синхри)
    synced_at    TEXT                -- коли ми останній раз оновили рядок
);
