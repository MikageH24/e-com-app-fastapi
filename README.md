# e-com-app-fastapi

Проект интернет-магазина на fastapi к курсу https://stepik.org/course/180000/promo

Установка:

1) python -m pip install -r requirements.txt - установка зависимостей

2) Подключение к бд postgresql

3) alembic revision --autogenerate -m "Initial migration" - создание миграции, чтобы создать в новой базе данных все необходимые таблицы

4) alembic upgrade head - выполнение миграции

5) uvicorn app.main:app --reload - запуск приложения
