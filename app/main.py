import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException, Query, Depends
from pydantic import ValidationError
from typing import List
import aiosqlite
from datetime import datetime
from .database import init_db, insert_review, get_reviews_by_sentiment
from .schemas import ReviewCreate, ReviewResponse
from .sentiment_analyzer import analyze_sentiment

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        await init_db()
        logger.info("База данных успешно инициализирована")
        yield
    except Exception as e:
        logger.error(f"Ошибка инициализации базы данных: {str(e)}")
        raise
    finally:
        logger.info("Приложение завершило работу")

app = FastAPI(title="Sentiment Analysis Service", lifespan=lifespan)

async def get_db():
    try:
        async with aiosqlite.connect("app/reviews.db") as db:
            db.row_factory = aiosqlite.Row
            yield db
    except aiosqlite.Error as e:
        logger.error(f"Ошибка подключения к базе данных: {str(e)}")
        raise HTTPException(status_code=500, detail="Ошибка подключения к базе данных")


@app.post("/reviews", response_model=ReviewResponse, status_code=201)
async def create_review(
    review: ReviewCreate, db: aiosqlite.Connection = Depends(get_db)
):
    try:
        if not review.text.strip():
            logger.warning("Получен пустой текст отзыва")
            raise HTTPException(
                status_code=422, detail="Текст отзыва не может быть пустым"
            )

        sentiment = analyze_sentiment(review.text)
        created_at = datetime.utcnow().isoformat()

        try:
            review_id = await insert_review(db, review.text, sentiment, created_at)
            await db.commit()
            logger.info(f"Отзыв создан с ID {review_id}")
            return ReviewResponse(
                id=review_id,
                text=review.text,
                sentiment=sentiment,
                created_at=created_at,
            )
        except aiosqlite.Error as e:
            await db.rollback()
            logger.error(f"Не удалось сохранить отзыв: {str(e)}")
            raise HTTPException(
                status_code=500, detail="Не удалось сохранить отзыв в базе данных"
            )
    except ValidationError as e:
        logger.warning(f"Некорректные данные: {str(e)}")
        raise HTTPException(status_code=422, detail=str(e))
    except Exception as e:
        logger.error(f"Непредвиденная ошибка при создании отзыва: {str(e)}")
        raise HTTPException(status_code=500, detail="Внутренняя ошибка сервера")


@app.get("/reviews", response_model=List[ReviewResponse])
async def get_reviews(
    sentiment: str = Query(None, pattern="^(positive|negative|neutral)$"),
    db: aiosqlite.Connection = Depends(get_db),
):
    try:
        if sentiment and sentiment not in {"positive", "negative", "neutral"}:
            logger.warning(f"Недопустимое значение тональности: {sentiment}")
            raise HTTPException(
                status_code=422,
                detail="Тональность должна быть 'positive', 'negative' или 'neutral'",
            )

        reviews = await get_reviews_by_sentiment(db, sentiment)
        logger.info(f"Получено {len(reviews)} отзывов с тональностью={sentiment}")
        return [
            ReviewResponse(
                id=r["id"],
                text=r["text"],
                sentiment=r["sentiment"],
                created_at=r["created_at"],
            )
            for r in reviews
        ]
    except aiosqlite.Error as e:
        logger.error(f"Ошибка базы данных при получении отзывов: {str(e)}")
        raise HTTPException(
            status_code=500, detail="Не удалось получить отзывы из базы данных"
        )
    except Exception as e:
        logger.error(f"Непредвиденная ошибка при получении отзывов: {str(e)}")
        raise HTTPException(status_code=500, detail="Внутренняя ошибка сервера")
