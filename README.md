# Bookish Corner Backend

Микросервисный backend для мобильного приложения для управления библиотекой аудио- и электронных книг.

---

# О проекте

Проект построен на микросервисной архитектуре с использованием:
- FastAPI
- PostgreSQL
- API Gateway
- GigaChat
- Google Books API

Основная цель проекта:
- хранение библиотеки книг;
- отслеживание прогресса чтения;
- трекер чтения и статистика;
- получение метаданных книг;
- AI-рекомендации через нейросеть.

---

# Архитектура

```text
Mobile Client
       ↓
API Gateway
       ↓
| Auth Service
| Library Service
| Progress Service
| Tracker Service
| Metadata Service
| Recommendation Service

```

Все сервисы взаимодействуют только через HTTP API.

Прямого доступа к БД других сервисов нет.

---

# Используемые технологии

## Backend
- Python 3.12
- FastAPI
- Pydantic
- PostgreSQL

## Архитектура
- Microservices
- API Gateway
- Repository Pattern
- Service Layer
- JWT Authentication

## External APIs
- Google Books API
- GigaChat API

## Infrastructure
- Docker
- Docker Compose
- RabbitMQ

---

# Микросервисы

## API Gateway

Единая точка входа для мобильного клиента.

### Функции
- маршрутизация запросов;
- проверка JWT;
- проксирование запросов между сервисами.

---

## Auth Service

Сервис авторизации и аутентификации пользователей.

### Функции
- регистрация;
- логин;
- JWT access token;
- refresh token;
- пользовательские сессии.

---

## Library Service

Сервис библиотеки книг.

### Функции
- создание книг;
- получение списка книг;
- получение книги по ID;
- обновление книг;
- удаление книг;
- работа с авторами и жанрами.

---

## Progress Service

Сервис прогресса чтения.

### Функции
- текущая глава;
- текущая позиция;
- процент прочтения;
- статус завершения книги.

---

## Tracker Service

Сервис пользовательской статистики.

### Функции
- reading goals;
- количество прочитанных книг;
- reading sessions;
- статистика чтения.

---

## Metadata Service

Сервис получения и кеширования метаданных книг.

### Функции
- интеграция с Google Books API;
- получение описаний и обложек.

---

## Recommendation Service

AI-сервис рекомендаций книг.

### Функции
- интеграция с GigaChat;
- рекомендации:
  - по жанру;
  - по стилю автора;
  - по атмосфере и сюжету;
- JSON-валидация ответов нейросети;
- кеширование рекомендаций.

---


Recommendation Service:
- получает информацию о книге;
- формирует prompt;
- валидирует JSON-ответ;
- кеширует рекомендации;
- возвращает результат клиенту.

---

# Структура сервисов

```text
service_name/
├── app/
│   ├── core/
│   ├── db/
│   ├── models/
│   ├── repositories/
│   ├── routers/
│   ├── schemas/
│   ├── services/
│   └── main.py
├── alembic/
├── Dockerfile
├── requirements.txt
└── alembic.ini
```

---

## Документация