# BIM360-Dashboard

🚀 **BIM360-Dashboard** — это веб-приложение для работы с проектами **Autodesk BIM 360** и **Autodesk Construction Cloud (ACC)**.  
Проект использует **FastAPI** на бэкенде, **React** на фронтенде и **PostgreSQL (Railway)** в качестве базы данных.

## 🔹 Функционал
### ✅ Версия 1 (MVP)
- Авторизация через **Autodesk APS OAuth 2.0**.
- Отображение списка **проектов** из **BIM 360** и **ACC**.
- Просмотр **папок и файлов** проекта.
- Отображение **истории активности** файлов (синхронизация, публикация, изменения).
- Извлечение **параметров элементов** Revit (для подсчета смет и анализа данных).

### 🚀 Версия 2 (AI-аналитика) — в разработке
- Автоматический анализ активности пользователей.
- Генерация отчетов по использованию BIM 360.
- Прогнозирование проблемных зон в проекте (ошибки синхронизации, неактуальные файлы).

### 🤖 Версия 3 (Автоматизация изменений) — в разработке
- Автоматическая корректировка параметров элементов Revit через **Revit API**.
- Интеграция **чат-бота в WhatsApp** для работы с файлами.
- **Автоматизация работы с BEP**.

---

## 🔹 Технологии
### **Бэкенд**: [FastAPI](https://fastapi.tiangolo.com/)  
- Python 3.9+
- FastAPI (быстрое асинхронное API)
- PostgreSQL (Railway)
- APS Autodesk API (BIM 360, ACC)
- JWT-токены

### **Фронтенд**: [React](https://reactjs.org/)  
- React + Vite
- TypeScript
- Tailwind CSS
- Zustand (для управления состоянием)
- Recharts (для графиков)

### **База данных**: [Railway](https://railway.app/)  
- PostgreSQL 14+
- Таблицы:
  - `users` — пользователи
  - `projects` — проекты
  - `files` — файлы в проектах
  - `activity` — действия с файлами
  - `revit_elements` — параметры элементов Revit

### **Хостинг**:
- **Бэкенд**: Railway
- **Фронтенд**: Vercel / Netlify

---

## 🔹 Структура проекта

BIM360-Dashboard/ │── backend/ # Бэкенд (FastAPI) │ ├── main.py # Запуск API │ ├── auth.py # Авторизация через Autodesk APS │ ├── database.py # Подключение к PostgreSQL (Railway) │ ├── models.py # Определение моделей БД │ ├── routes/ # API-эндпоинты │ │ ├── projects.py # Получение проектов │ │ ├── files.py # Получение файлов и активности │ │ ├── elements.py # Данные по элементам Revit │ │ ├── sync.py # Синхронизация данных │ ├── services/ # Запросы к Autodesk BIM 360 API │ ├── utils.py # Вспомогательные функции │ ├── requirements.txt # Зависимости Python │── frontend/ # Фронтенд (React) │ ├── src/ │ │ ├── components/ # UI-компоненты │ │ ├── pages/ │ │ │ ├── Login.jsx # Авторизация │ │ │ ├── Dashboard.jsx # Панель управления │ │ │ ├── Projects.jsx # Список проектов │ │ │ ├── Files.jsx # Список файлов │ │ │ ├── Activity.jsx # История активности │ ├── App.js # Основной файл React │ ├── package.json # Зависимости React │── .env # Конфигурация (APS_CLIENT_ID, APS_SECRET) │── docker-compose.yml # Опционально, если локальный запуск │── README.md # Этот файл

yaml
Копировать

---

## 🔹 Установка и запуск

### 1️⃣ **Клонирование репозитория**
```bash
git clone https://github.com/YOUR_GITHUB/BIM360-Dashboard.git
cd BIM360-Dashboard
2️⃣ Настройка переменных окружения
Создайте .env файл и добавьте в него:

ini
Копировать
APS_CLIENT_ID=ваш_клиентский_ID
APS_CLIENT_SECRET=ваш_секретный_ключ
RAILWAY_DATABASE_URL=postgresql://user:password@host:port/database
3️⃣ Запуск бэкенда
bash
Копировать
cd backend
pip install -r requirements.txt
uvicorn main:app --reload
Бэкенд будет доступен на:
🔗 http://127.0.0.1:8000/docs

4️⃣ Запуск фронтенда
bash
Копировать
cd frontend
npm install
npm run dev
Фронтенд будет доступен на:
🔗 http://localhost:5173

🔹 API-эндпоинты
Метод	URL	Описание
GET	/auth/login	Авторизация через Autodesk APS
GET	/projects	Получение списка проектов
GET	/projects/{project_id}/files	Файлы проекта
GET	/files/{file_id}/activity	История активности файла
GET	/files/{file_id}/parameters	Параметры элементов Revit
🔹 Деплой
Бэкенд на Railway
Авторизуйтесь на Railway.app.
Создайте новый проект и подключите PostgreSQL.
Загрузите код FastAPI через GitHub.
Добавьте переменные окружения (APS_CLIENT_ID, APS_SECRET, RAILWAY_DATABASE_URL).
Нажмите "Deploy".
Фронтенд на Vercel
Авторизуйтесь на Vercel.
Подключите репозиторий.
Выберите frontend как корневую папку.
Настройте переменные окружения (API_URL).
Запустите деплой.
🔹 Будущие улучшения
🔥 AI-анализ активности в BIM 360.
🔥 Интеграция чат-бота WhatsApp.
🔥 Автоматизация работы с файлами Revit.
💡 Разработка ведётся! Присоединяйтесь 🚀

🚀 Пошаговая инструкция: Как получить данные из Autodesk API
Этот процесс НЕ изменяет файл — он только получает данные.

✅ Шаг 1: Получаем Access Token
Ты уже умеешь это делать. В коде ниже он получается автоматически.

✅ Шаг 2: Кодируем URN в base64
URN уже есть:

plaintext
Копировать
Редактировать
urn:adsk.wipprod:dm.lineage:fDxvKYmvREOxMGFYUk6VaQ
Его нужно закодировать в base64, удалив лишние символы (= в конце).

✅ Шаг 3: Отправляем файл на перевод
Чтобы получить данные из файла, его надо перевести в формат, который можно анализировать (SVF).

✅ Шаг 4: Ожидаем завершения перевода
Нужно дождаться, пока Model Derivative API переведёт файл.

✅ Шаг 5: Получаем метаданные
Метаданные содержат GUID, который понадобится дальше.

✅ Шаг 6: Получаем свойства файла
Через API загружаем свойства, ищем Project Base Point.



📌 Итоговая последовательность:
1️⃣ Получаем токен → get_access_token()
2️⃣ Кодируем URN в base64 → encode_urn(urn)
3️⃣ Запускаем перевод файла → send_translation_request(access_token, base64_urn)
4️⃣ Ожидаем завершения перевода → wait_for_translation(access_token, base64_urn)
5️⃣ Получаем метаданные (ищем GUID) → get_metadata(access_token, base64_urn)
6️⃣ Получаем свойства для GUID → get_properties(access_token, base64_urn, guid)
7️⃣ Извлекаем Project Base Point → extract_project_base_point(properties)



Проблема с "Ошибка перевода: Token does not have the privilege for this request"
Сейчас в scope у тебя есть:

✅ data:read (Чтение данных)
✅ data:write (Запись данных)
✅ data:create (Создание данных)
✅ bucket:create (Создание бакетов)
✅ code:all (Доступ ко всем API Forge для кода)
Но не хватает прав для Model Derivative API! 🛑
Тебе нужно добавить:

data:read
data:write
data:create
bucket:read ⬅ Нужно для работы с файлами!
bucket:update ⬅ Для запуска перевода файлов!
data:search ⬅ В некоторых сценариях Model Derivative API требует это право!


