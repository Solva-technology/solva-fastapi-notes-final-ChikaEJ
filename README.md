# 📝 FastAPI Notes App

## 📘 Описание проекта
**FastAPI Notes App** — это backend-приложение для создания и управления заметками.  
Приложение реализовано на **FastAPI** с использованием **PostgreSQL**, **SQLAlchemy**, **Alembic** и **FastAPI Users** для аутентификации и авторизации.  
Проект полностью контейнеризирован с помощью **Docker** и запускается одной командой.

---

## 🧩 Цели и особенности
- CRUD-операции для заметок (создание, чтение, обновление, удаление)
- Привязка заметок к конкретным пользователям
- Авторизация и регистрация через JWT
- Разделение прав (пользователь / администратор)
- Публичные заметки с возможностью просмотра другими пользователями
- Асинхронная работа с базой данных PostgreSQL
- Контейнеризация и автоматическое применение миграций при старте

---

## 📂 Структура проекта
```
app/
│── api/
│   ├── endpoints/
│   │   ├── notes.py
│   │   └── users.py
│   ├── schemas/
│   │   ├── notes.py
│   │   └── users.py
│   ├── __init__.py
│   └── routers.py
│
│── core/
│   ├── base.py
│   ├── config.py
│   ├── constants.py
│   ├── db.py
│   └── __init__.py
│
│── db/
│   ├── crud/
│   │   └── notes.py
│   ├── models/
│   │   ├── note.py
│   │   └── user.py
│   └── __init__.py
│
│── main.py
│── alembic/
│── alembic.ini
│── Dockerfile
│── docker-compose.yml
│── entrypoint.sh
```

---

## ⚙️ Конфигурация и база данных
Настройки проекта находятся в `core/config.py`.  
Подключение к базе данных выполняется через **SQLAlchemy**, а миграции управляются с помощью **Alembic**.

```python
SQLALCHEMY_DATABASE_URL = "postgresql+asyncpg://user:password@db:5432/notes_db"
```

`core/db.py` содержит асинхронный движок и сессию SQLAlchemy.

---

## 🧱 Модели

### Note (`db/models/note.py`)
```python
class Note(Base):
    __tablename__ = "notes"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    content = Column(Text, nullable=False)
    is_public = Column(Boolean, default=False)
    is_completed = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    owner_id = Column(UUID(as_uuid=True), ForeignKey("user.id"), nullable=False)

    owner = relationship("User", back_populates="notes")
```

### User (`db/models/user.py`)
Модель пользователя реализована с помощью **FastAPI Users**  
и содержит стандартные поля (`id`, `email`, `hashed_password`, `is_active`, `is_superuser`, и т.д.).

---

## 🧾 Схемы (Pydantic)

### Пример схемы для заметок
```python
class NoteCreate(BaseModel):
    title: str
    content: str
    is_public: bool = False
    is_completed: bool = False
```

```python
class NoteRead(NoteCreate):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True
```

Также реализованы схемы пользователей (`UserCreate`, `UserRead`).

---

## 🔧 CRUD-операции
Функции для взаимодействия с базой данных находятся в `db/crud/notes.py`.

Пример:
```python
async def create_note(session: AsyncSession, note_data: NoteCreate, user_id: int):
    note = Note(**note_data.dict(), owner_id=user_id)
    session.add(note)
    await session.commit()
    await session.refresh(note)
    return note
```

Остальные функции (`get_notes`, `get_note`, `update_note`, `delete_note`)  
фильтруют данные по `owner_id`, что гарантирует доступ только к заметкам текущего пользователя.

---

## 🌐 API и маршруты

### Основные эндпоинты `/notes`

| Метод | Эндпоинт | Описание | Авторизация |
|--------|-----------|-----------|--------------|
| `POST` | `/notes/` | Создать новую заметку | ✅ |
| `GET` | `/notes/` | Получить список своих заметок | ✅ |
| `GET` | `/notes/{note_id}` | Получить заметку по ID | ✅ |
| `PATCH` | `/notes/{note_id}` | Обновить заметку | ✅ |
| `DELETE` | `/notes/{note_id}` | Удалить заметку | ✅ |
| `GET` | `/notes/global` | Список публичных заметок других пользователей (пагинация) | ✅ |
| `GET` | `/user/notes/{user_id}` | Заметки конкретного пользователя | ✅ / 🔒 Админ |

Все эндпоинты используют зависимость `Depends(current_user)` для получения текущего пользователя.

---

## 🔐 Авторизация и пользователи
Авторизация реализована с помощью **FastAPI Users**.  
Используется JWT-аутентификация (access/refresh токены).

### Возможности
- Регистрация нового пользователя
- Авторизация и получение токенов
- Обновление токена
- Просмотр и редактирование собственного профиля
- Разграничение прав (обычный пользователь / администратор)

Администратор имеет полные права на:
- Просмотр и редактирование любых заметок
- Удаление записей пользователей

---

## 🐳 Docker
Проект полностью контейнеризирован и готов к развертыванию.

### Сервисы
- **web** — FastAPI-приложение
- **db** — PostgreSQL
- **migration** — Alembic (автоматически применяет миграции при запуске)

### Запуск проекта
```bash
docker-compose up --build
```

После сборки приложение будет доступно по адресу:
```
http://localhost:8000
```

---

## 🧠 Технологический стек
- **Python 3.11+**
- **FastAPI**
- **SQLAlchemy (async)**
- **Alembic**
- **PostgreSQL**
- **FastAPI Users**
- **Docker / Docker Compose**
- **Pydantic**

---

## 🚀 Функциональность
✅ CRUD для заметок  
✅ Авторизация через JWT  
✅ Привязка заметок к пользователю  
✅ Публичные и приватные заметки  
✅ Роли пользователей (user / admin)  
✅ Асинхронная работа с БД  
✅ Контейнеризация и миграции  
✅ Пагинация публичных записей  

---

## 📦 Команды для разработки

### Запуск приложения локально
```bash
uvicorn app.main:app --reload
```

### Создание миграций Alembic
```bash
alembic revision --autogenerate -m "Init migration"
alembic upgrade head
```

### Остановка контейнеров
```bash
docker-compose down
```

---

## 🧾 Итог
**FastAPI Notes App** — это готовое, модульное и расширяемое решение  
для управления пользовательскими заметками с безопасной авторизацией,  
разделением прав доступа и полной поддержкой Docker.
