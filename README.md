## Установка

1. Клонируйте репозиторий:
```bash
git clone https://github.com/Harakirigi/sentiment_service
cd sentiment_service
```
2. Создайте виртуальное окружение
На Windows:
```bash
python -m venv venv
venv\Scripts\activate
```
Или на linux:
```bash
python -m venv venv
source venv/bin/activate
```
3. Установите зависимости
```bash
pip install -r requirements.txt
```
4. Запустите сервис
```bash
python -m uvicorn app.main:app --reload
```
# API

## POST /reviews
Создаёт отзыв и определяет его тональность
Запрос:
```bash
curl -X POST "http://localhost:8000/reviews" -H "Content-Type: application/json" -d '{"text": "Отличный сервис!"}'
```
Ответ (201):
```json
{
  "id": 1,
  "text": "Отличный сервис!",
  "sentiment": "positive",
  "created_at": "2025-07-20T10:02:34.123456"
}
```
Ошибки:
- 422: Пустой или слишком длинный отзыв ("detail": "Текст отзыва не может быть пустым", "ensure this value has at most 1000 characters").
- 500: Ошибка базы данных ("detail": "Не удалось сохранить отзыв в базе данных").
## GET /reviews
Возвращает отзывы (можно фильтровать по sentiment=positive|negative|neutral)
Запрос:
```bash
curl "http://localhost:8000/reviews?sentiment=negative"
```
Ответ (200):
```json
[
  {
    "id": 2,
    "text": "Ужасный сервис!",
    "sentiment": "negative",
    "created_at": "2025-07-20T10:03:45.678901"
  }
]
```
Ошибки:
- 422: Неверная тональность ("detail": "Тональность должна быть 'positive', 'negative' или 'neutral'").
- 500: Ошибка базы данных ("detail": "Не удалось получить отзывы из базы данных").