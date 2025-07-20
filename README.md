## Установка

Клонируйте репозиторий:
```bash
git clone https://github.com/Harakirigi/sentiment_service
cd sentiment_service
```
## Создайте виртуальное окружение

python -m venv venv
venv\Scripts\activate
# или на linux:
source venv/bin/activate

## Установите зависимости

pip install -r requirements.txt

## Установите зависимости

python -m uvicorn app.main:app --reload

## API

# POST /reviews
Запрос:
curl -X POST "http://localhost:8000/reviews" -H "Content-Type: application/json" -d '{"text": "Отличный сервис!"}'
Ответ (201):
{
  "id": 1,
  "text": "Отличный сервис!",
  "sentiment": "positive",
  "created_at": "2025-07-20T10:02:34.123456"
}

# GET /reviews
Запрос:
curl "http://localhost:8000/reviews?sentiment=negative"
Ответ (200):
[
  {
    "id": 2,
    "text": "Ужасный сервис!",
    "sentiment": "negative",
    "created_at": "2025-07-20T10:03:45.678901"
  }
]