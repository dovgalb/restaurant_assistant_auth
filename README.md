Команды для инициализации poetry

1. Установка poetry. Запускать на окружении системы(не виртуальное.)

```pip install poetry```

2. Активируем виртуальное окружение

```poetry shell```

3. Устанавливаем зависимости

```poetry install```

4. Если надо добавить зависимостей 

```poetry add "library_name"```


Команды для alembic
1. Создание миграций(Если миграции уже есть, перейти к следующему пункту)

```alembic revision --autogenerate -m 'commit-text'```

2. Применение миграций

```alembic upgrade head```


Запуск сервера uvicorn

```uvicorn main:app --reload```