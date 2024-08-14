# e-com-app-fastapi

Проект интернет-магазина на fastapi к курсу https://stepik.org/course/180000/promo

Запуск:

1) docker compose -f docker-compose.prod.yml up -d --build - сборка образа и поднятие контейнеров
2) docker compose -f docker-compose.prod.yml exec web alembic upgrade head - миграция для создания структуры бд

Остановка контейнеров

1) docker-compose down -v 

