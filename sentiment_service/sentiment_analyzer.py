import logging

logger = logging.getLogger(__name__)

POSITIVE_WORDS = {
    "хорош": 1.0,
    "люблю": 1.2,
    "отличн": 1.5,
    "прекрасн": 1.5,
    "замечательн": 1.5,
}
NEGATIVE_WORDS = {
    "плохо": 1.0,
    "ненавиж": 1.5,
    "ужасн": 1.5,
    "проблем": 1.2,
    "отстой": 1.3,
}

def analyze_sentiment(text: str) -> str:
    try:
        if not text or not isinstance(text, str):
            logger.warning(
                "Неверный ввод для анализа тональности: пустой текст или текст, не содержащий строк"
            )
            return "neutral"

        text_lower = text.lower()
        positive_score = 0.0
        negative_score = 0.0

        for word, weight in POSITIVE_WORDS.items():
            if word in text_lower:
                positive_score += weight * text_lower.count(word)
        for word, weight in NEGATIVE_WORDS.items():
            if word in text_lower:
                negative_score += weight * text_lower.count(word)

        if positive_score > negative_score + 0.5:
            return "positive"
        elif negative_score > positive_score + 0.5:
            return "negative"
        return "neutral"
    except Exception as e:
        logger.error(f"Ошибка в анализе настроений: {str(e)}")
        return "neutral"
