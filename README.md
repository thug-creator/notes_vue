# Техническая документация проекта Notes (Django + Vue.js)
Проект представляет собой классическое разделение на Stateless API (Backend) и SPA (Frontend).
## 🧠 Серверная часть: Архитектура Django
<img width="261" height="466" alt="image" src="https://github.com/user-attachments/assets/14adbe1e-f1b2-4e80-aeb2-6e1f90a00e13" />

Бэкенд построен на Django REST Framework (DRF), что позволяет отдавать данные в формате JSON.
1. Модель данных (models.py)
<img width="627" height="466" alt="image" src="https://github.com/user-attachments/assets/63c4c3bd-4997-459f-a2d7-79dc5c327f95" />

Основная сущность — Note.
Поля: title (Char), content (Text), created_at (DateTime), updated_at (DateTime).
Опционально: Связь User (ForeignKey), если реализована авторизация.
2. Слой сериализации (serializers.py)

Используется ModelSerializer для преобразования объектов базы данных в JSON и валидации входящих данных от фронтенда перед сохранением.
3. API Endpoints (views.py & urls.py)
<img width="597" height="516" alt="image" src="https://github.com/user-attachments/assets/2aa9936d-d9d6-49ab-946a-046cf9b11cb8" />
<img width="731" height="212" alt="image" src="https://github.com/user-attachments/assets/51bfd13b-dc57-406d-9db4-59ba9f7f8d05" />

Используются либо APIView, либо ModelViewSet для реализации стандартных операций:
GET /api/notes/ — получение списка всех заметок.
POST /api/notes/ — создание новой заметки.
GET /api/notes/<id>/ — детали конкретной заметки.
PUT/PATCH /api/notes/<id>/ — редактирование.
DELETE /api/notes/<id>/ — удаление.
4. Настройки CORS (settings.py)
import os
from pathlib import Path
from datetime import timedelta

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-your-secret-key-here'

DEBUG = True

ALLOWED_HOSTS = ['localhost', '127.0.0.1']

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # Third party
    'rest_framework',
    'rest_framework_simplejwt',
    'corsheaders',
    
    # Local
    'notes',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'backend.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'backend.wsgi.application'

#База данных (SQLite для простоты)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

#Настройки DRF
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
}

#Настройки JWT
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=60),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
}

#CORS
CORS_ALLOWED_ORIGINS = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

LANGUAGE_CODE = 'ru-ru'
TIME_ZONE = 'Europe/Moscow'
USE_I18N = True
USE_TZ = True

STATIC_URL = 'static/'
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

Для работы с Vue (который обычно запускается на порту 8080) в Django подключен пакет django-cors-headers.
В INSTALLED_APPS добавлен corsheaders.
В MIDDLEWARE слой CorsMiddleware стоит выше CommonMiddleware.
CORS_ALLOWED_ORIGINS настроен на адрес фронтенда.
## 🖥 Клиентская часть: Архитектура Vue.js
<img width="268" height="442" alt="image" src="https://github.com/user-attachments/assets/09cb6a75-ea5b-407e-a22e-e4e28ab4bd46" />

Фронтенд представляет собой компонентную структуру.
1. Управление состоянием и данными
Взаимодействие с API вынесено в отдельный слой (обычно это папка services/ или прямо в методах компонентов через Axios).
Base URL: Все запросы идут на http://localhost:8000/api/.
Жизненный цикл: Загрузка данных происходит в хуке mounted() или created().
2. Компонентная структура
App.vue — корневой компонент.
NoteList.vue — отвечает за отображение списка (использует v-for для итерации по массиву заметок).
NoteItem.vue — отдельная карточка заметки.
NoteForm.vue — форма создания/редактирования с использованием v-model для двусторонней связки данных.
3. Реактивность
При удалении или добавлении заметки фронтенд не перезагружает страницу. Вместо этого:
Отправляется запрос к API.
При успешном ответе (HTTP 200/201/204) локальный массив заметок в Vue обновляется методом .push(), .filter() или повторным запросом списка.
🔄 Протокол взаимодействия (Data Flow)
Запрос данных: Vue (Axios) GET -> Django URL -> View -> Serializer -> DB.
Ответ данных: DB -> Serializer -> JSON -> Vue (State) -> Virtual DOM Update.
Обработка ошибок: Бэкенд возвращает ошибки валидации (например, 400 Bad Request), которые перехватываются catch в Axios и выводятся пользователю через v-if или алерты.
🛠 Инструкция по развертыванию (Dev Mode)
Бэкенд:
bash
## Создание миграций под схему данных
1. python manage.py makemigrations
2. python manage.py migrate

## Создание админки для ручного управления заметками
1. python manage.py createsuperuser

Фронтенд:
Для корректной работы убедитесь, что в файлах .vue или api.js указан верный адрес сервера:
javascript
axios.defaults.baseURL = 'http://127.0.0.1:8000';
