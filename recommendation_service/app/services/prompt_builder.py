from ..schemas.recommendation import RecommendationMode, RecommendationRequest


class PromptBuilder:
    @staticmethod
    def build_prompt(data: RecommendationRequest) -> str:
        book = data.source_book

        base = f"""
Ты — рекомендательная система для приложения электронных и аудиокниг.

Тебе нужно вернуть СТРОГО JSON без markdown, без пояснений и без текста вокруг.

Формат ответа:
{{
  "recommendations": [
    {{
      "title": "Название книги",
      "author": "Автор",
      "reason": "Краткое объяснение, почему книга подходит",
      "similarity_type": "genre | author_style | plot_atmosphere",
      "confidence": 0.0,
      "search_query": "Название книги Автор"
    }}
  ]
}}

Правила:
- Верни ровно {data.count} книг.
- Не возвращай исходную книгу.
- Не выдумывай несуществующие книги.
- У каждой книги обязательно должны быть title, author, reason, similarity_type, confidence, search_query.
- confidence должен быть числом от 0 до 1.
- Ответ должен быть валидным JSON.
- Никакого markdown.
"""

        book_info = f"""
Исходная книга:
Название: {book.title}
Автор: {book.author or "не указан"}
Жанр: {book.genre or "не указан"}
Описание/аннотация: {book.description or "не указано"}
"""

        if data.mode == RecommendationMode.SAME_GENRE:
            task = """
Задача:
Подбери книги в том же или максимально близком жанре.
Главный критерий — жанровое сходство.
"""
        elif data.mode == RecommendationMode.AUTHOR_STYLE:
            task = """
Задача:
Подбери книги, похожие по стилю автора.
Учитывай манеру повествования, темп, язык, эмоциональность, композицию и тип конфликта.
"""
        else:
            task = """
Задача:
Подбери книги с похожим сюжетом, атмосферой и эмоциональным ощущением.
Учитывай настроение, темы, динамику, сеттинг и впечатление от чтения.
"""

        return base + book_info + task