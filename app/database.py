import aiosqlite
import logging

logger = logging.getLogger(__name__)

async def init_db():
    try:
        async with aiosqlite.connect("app/reviews.db") as db:
            await db.execute(
                """
                CREATE TABLE IF NOT EXISTS reviews (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    text TEXT NOT NULL,
                    sentiment TEXT NOT NULL,
                    created_at TEXT NOT NULL
                )
            """
            )
            await db.commit()
    except aiosqlite.Error as e:
        logger.error(f"Ошибка инициализации базы данных: {str(e)}")
        raise

async def insert_review(
    db: aiosqlite.Connection, text: str, sentiment: str, created_at: str
) -> int:
    try:
        cursor = await db.execute(
            "INSERT INTO reviews (text, sentiment, created_at) VALUES (?, ?, ?)",
            (text, sentiment, created_at),
        )
        return cursor.lastrowid
    except aiosqlite.Error as e:
        logger.error(f"Не удалось добавить отзыв: {str(e)}")
        raise


async def get_reviews_by_sentiment(
    db: aiosqlite.Connection, sentiment: str = None
) -> list:
    try:
        if sentiment:
            cursor = await db.execute(
                "SELECT id, text, sentiment, created_at FROM reviews WHERE sentiment = ?",
                (sentiment,),
            )
        else:
            cursor = await db.execute(
                "SELECT id, text, sentiment, created_at FROM reviews"
            )
        return await cursor.fetchall()
    except aiosqlite.Error as e:
        logger.error(f"Не удалось получить отзывы: {str(e)}")
        raise
