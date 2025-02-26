# ДОСКА ОБЬЯВЛЕНИЙ

Backend-часть для сайта объявлений.

## ФУНКЦИОНАЛ:

* Авторизация и аутентификация пользователей.
* Распределение ролей между пользователями (пользователь и админ).
* Восстановление пароля через электронную почту.
* CRUD для объявлений на сайте (админ может удалять или редактировать все объявления, а пользователи только свои).
* Под каждым объявлением пользователи могут оставлять отзывы.
* В заголовке сайта можно осуществлять поиск объявлений по названию.

В проекте используются следующие зависимости:

* django
* djangorestframework
* djangorestframework-simplejwt
* django-cors-headers
* drf-yasg
* psycopg2-binary
* python-dotenv
* pillow
* django-filter
* docker
* pytest
* pytest-django
* pytest-cov
* celery
* django-celery-beat
* redis

Для разработки дополнительно:

* flake8
* black
* isort

## ДЛЯ НАЧАЛА РАБОТЫ:

* Скачать репозиторий: https://github.com/Irina-Prokopova-01/SB1_diplom

* Применить все зависимости с файла pyproject.toml
(команда: poetry add pyproject.toml).

* Создать файл .env и внести все чувствительные параметры указанные в файле .env.sample

* Для работы celery запустите redis сервер
(команда: redis-server) и далее (команда: celery -A config worker --beat --scheduler django --loglevel=info)

* Если есть надобность задеплоить проект на Docker
(команда: docker-compose up -d --build)


### Имеются тесты на весь функционал проекта

