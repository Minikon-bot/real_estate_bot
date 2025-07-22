import asyncpg
import os

DATABASE_URL = os.getenv("DATABASE_URL")

async def init_db():
    conn = await asyncpg.connect(DATABASE_URL)
    await conn.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            tg_id BIGINT UNIQUE,
            filters JSONB
        );
    """)
    await conn.execute("""
        CREATE TABLE IF NOT EXISTS listings (
            id SERIAL PRIMARY KEY,
            url TEXT UNIQUE,
            title TEXT,
            price TEXT,
            location TEXT,
            description TEXT,
            image_url TEXT,
            hash TEXT UNIQUE
        );
    """)
    await conn.close()

async def add_user(tg_id):
    conn = await asyncpg.connect(DATABASE_URL)
    await conn.execute(
        "INSERT INTO users (tg_id, filters) VALUES ($1, $2) ON CONFLICT (tg_id) DO NOTHING",
        tg_id, {}
    )
    await conn.close()

async def get_users():
    conn = await asyncpg.connect(DATABASE_URL)
    users = await conn.fetch("SELECT tg_id FROM users")
    await conn.close()
    return [u['tg_id'] for u in users]

async def listing_exists(hash_id):
    conn = await asyncpg.connect(DATABASE_URL)
    exists = await conn.fetchrow("SELECT 1 FROM listings WHERE hash = $1", hash_id)
    await conn.close()
    return exists is not None

async def add_listing(ad):
    conn = await asyncpg.connect(DATABASE_URL)
    await conn.execute("""
        INSERT INTO listings (url, title, price, location, description, image_url, hash)
        VALUES ($1, $2, $3, $4, $5, $6, $7)
    """, ad["url"], ad["title"], ad["price"], ad["location"], ad["description"], ad["image_url"], ad["hash"])
    await conn.close()
