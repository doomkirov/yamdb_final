![Yamdb workflow status](https://github.com/doomkirov/yamdb_final/actions/workflows/yamdb_workflow.yml/badge.svg)
# API_YAMDB
REST API проект для сервиса YaMDb — тут пользователи могут оставлять свои обзоры и отзывы на различные произведения искусства.

## Описание

Проект YaMDb собирает отзывы пользователей на произведения.
Произведения делятся на различные категории, список которых может постоянно дополняться.
### Как запустить проект:

Если вы пользуетесь Windows, убедитесь в наличии у Вас установленного и работающего Docker.

Клонируем репозиторий и переходим в него:
```bash
git clone https://github.com/themasterid/infra_sp2
cd infra_sp2
cd infra
```

Поднимаем контейнеры (infra_db_1, infra_web_1, infra_nginx_1):
```bash
docker-compose up -d --build
```

Выполняем миграции:
```bash
docker-compose exec web python manage.py makemigrations reviews
```
```bash
docker-compose exec web python manage.py migrate
```

Создаем суперпользователя:
```bash
docker-compose exec web python manage.py createsuperuser
```

Србираем статику:
```bash
docker-compose exec web python manage.py collectstatic --no-input
```

Заполняем базу данных файлами из static/data/*.csv
```bash
docker-compose exec web python manage.py load_data
```

Создаем дамп базы данных (нет в текущем репозитории):
```bash
docker-compose exec web python manage.py dumpdata > fixtures.json
```

Останавливаем и удаляем контейнеры:
```bash
docker-compose down -v
```

### Файл .env, который должен быть в папке infra/ (шаблон наполнения)
```
DB_ENGINE=django.db.backends.postgresql
DB_NAME=postgres
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
DB_HOST=db
DB_PORT=5432
```

### Документация API YaMDb
Документация доступна по эндпойнту: http://localhost/redoc/

### Автор
Проект выполнен совместно тремя студентами курса Python-разработчик Яндек.Практикума.
В их числе и я - Шилов Иван. Занимался разработкой моделей, файла view, реализацией 
импорта данных из csv-файлов, а так же настраивал эндпоинты для произведений, категорий, жанров.

### Доступность проекта
http://doomnewera.ddns.net