# 🇺🇦 Українська версія

# REST API для керування контактами (Contacts API)

Асинхронний вебзастосунок на базі **FastAPI** та **SQLAlchemy 2.0**, призначений для збереження, пошуку та керування контактами. Застосунок використовує базу даних **PostgreSQL** (через драйвер `asyncpg`) для збереження інформації та **Alembic** для керування міграціями.

---

## 🛠 Технологічний стек
* **Python 3.10+**
* **FastAPI** (ASGI вебфреймворк)
* **SQLAlchemy 2.0** (ORM з підтримкою асинхронного режиму)
* **PostgreSQL** + **asyncpg** (СУБД та асинхронний драйвер)
* **Alembic** (інструмент для міграцій бази даних)
* **Pydantic v2** (валідація вхідних та вихідних даних)
* **Poetry** (керування віртуальним середовищем та залежностями)

---

## 🚀 Інструкція із запуску

### 1. Клонування проєкту та встановлення залежностей
Переконайтеся, що у вас встановлено інструмент **Poetry**.

1. Клонуйте репозиторій та перейдіть у робочу директорію проєкту:
   ```bash
   git clone <url_репозиторію>
   cd goit-pythonweb-hw-10
   ```
2. Встановіть залежності за допомогою Poetry:
   ```bash
   poetry install
   ```
3. Активуйте віртуальне середовище:
   ```bash
   poetry shell
   ```

---

### 2. Налаштування бази даних та змінних оточення

Для роботи застосунку потрібна запущена база даних PostgreSQL. Ви можете використовувати локальний сервер PostgreSQL або запустити контейнер через Docker.

#### Запуск бази даних у Docker (якщо встановлено Docker)
```bash
docker run --name contacts-db -e POSTGRES_USER=postgres -e POSTGRES_PASSWORD=mysecretpassword -e POSTGRES_DB=contacts_api -p 5432:5432 -d postgres
```

#### Налаштування файлу `.env`
Створіть у кореневій папці проєкту файл **`.env`** та додайте параметри підключення до вашої бази даних.
> **Зверніть увагу:** Оскільки застосунок працює асинхронно, протокол підключення має починатися з `postgresql+asyncpg://`.

```ini
DATABASE_URL=postgresql+asyncpg://postgres:mysecretpassword@localhost:5432/contacts_api
```

Переконайтеся, що у вашому файлі `alembic.ini` (або `migrations/env.py`) налаштовано отримання URL саме з цієї змінної оточення.

---

### 3. Застосування міграцій Alembic
Перед запуском програми необхідно налаштувати таблиці в базі даних за допомогою міграцій.

Застосуйте всі наявні міграції до бази даних:
```bash
poetry run alembic upgrade head
```

---

### 4. Запуск застосунку
Запустити сервер FastAPI можна за допомогою команди:

```bash
poetry run python main.py
```

Сервер запуститься за адресою: **`http://127.0.0.1:8001`**.

---

## 📖 Документація API

Після успішного запуску сервера інтерактивна документація доступна за посиланнями:
* **Swagger UI:** [http://127.0.0.1:8001/docs](http://127.0.0.1:8001/docs)

### Основні доступні маршрути (Endpoints)

| Метод | Маршрут | Опис |
| :--- | :--- | :--- |
| **GET** | `/api/healthchecker` | Перевірка працездатності та з'єднання з базою даних |
| **GET** | `/api/contacts/` | Отримання списку контактів (з підтримкою пагінації та фільтрації за `first_name`, `last_name`, `email`) |
| **GET** | `/api/contacts/birthdays` | Отримання контактів, у яких день народження буде у найближчі 7 днів |
| **GET** | `/api/contacts/{contact_id}` | Отримання детальної інформації про конкретний контакт |
| **POST** | `/api/contacts/` | Створення нового контакту (поля `email` мають бути унікальними) |
| **PATCH** | `/api/contacts/{contact_id}` | Оновлення окремих полів наявного контакту |
| **DELETE** | `/api/contacts/{contact_id}` | Видалення контакту з бази даних |


---
___
___

# 🇺🇸 English Version

# REST API for Contact Management (Contacts API)

An asynchronous web application built with **FastAPI** and **SQLAlchemy 2.0**, designed for storing, searching, and managing contacts. The application utilizes a **PostgreSQL** database (via the `asyncpg` driver) for data storage and **Alembic** for managing database migrations.

---

## 🛠 Technology Stack
* **Python 3.10+**
* **FastAPI** (ASGI web framework)
* **SQLAlchemy 2.0** (ORM with asynchronous support)
* **PostgreSQL** + **asyncpg** (DBMS and asynchronous driver)
* **Alembic** (database migration tool)
* **Pydantic v2** (input and output data validation)
* **Poetry** (dependency and virtual environment management)

---

## 🚀 Getting Started

### 1. Clone the Project and Install Dependencies
Ensure you have **Poetry** installed on your system.

1. Clone the repository and navigate to the project directory:
   ```bash
   git clone <repository_url>
   cd goit-pythonweb-hw-10
   ```
2. Install dependencies using Poetry:
   ```bash
   poetry install
   ```
3. Activate the virtual environment:
   ```bash
   poetry shell
   ```

---

### 2. Database Setup and Environment Variables

The application requires a running PostgreSQL database. You can use a local PostgreSQL server or run a database container via Docker.

#### Running PostgreSQL in Docker (Alternative)
```bash
docker run --name contacts-db -e POSTGRES_USER=postgres -e POSTGRES_PASSWORD=mysecretpassword -e POSTGRES_DB=contacts_api -p 5432:5432 -d postgres
```

#### Configuring the `.env` File
Create a **`.env`** file in the root directory of the project and add your database connection parameters.
> **Note:** Since the application runs asynchronously, the connection protocol must start with `postgresql+asyncpg://`.

```ini
DATABASE_URL=postgresql+asyncpg://postgres:mysecretpassword@localhost:5432/contacts_api
```

Ensure that your `alembic.ini` (or `migrations/env.py`) file is configured to retrieve the database URL from this environment variable.

---

### 3. Applying Alembic Migrations
Before running the application, you must set up the database tables using migrations.

Apply all existing migrations to your database:
```bash
poetry run alembic upgrade head
```

---

### 4. Running the Application
You can start the FastAPI server with the following command:

```bash
poetry run python main.py
```

The server will automatically start at **`http://127.0.0.1:8001`**.

---

## 📖 API Documentation

Once the server is running, the interactive documentation is available at:
* **Swagger UI:** [http://127.0.0.1:8001/docs](http://127.0.0.1:8001/docs)

### Key API Endpoints

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| **GET** | `/api/healthchecker` | Verifies the database connection and service health status |
| **GET** | `/api/contacts/` | Retrieves a list of contacts (supports pagination and filtering by `first_name`, `last_name`, `email`) |
| **GET** | `/api/contacts/birthdays` | Retrieves contacts who have birthdays within the next 7 days |
| **GET** | `/api/contacts/{contact_id}` | Retrieves details for a specific contact |
| **POST** | `/api/contacts/` | Creates a new contact (`email` values must be unique) |
| **PATCH** | `/api/contacts/{contact_id}` | Updates specific fields of an existing contact |
| **DELETE** | `/api/contacts/{contact_id}` | Deletes a contact from the database |