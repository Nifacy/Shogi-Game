# Описание проекта

Проект представляет собой веб сервис для мультиплеерной игры в пошаговую игру "Сеги". Компоненты проекта реализованы на основе
библиотек fastapi и aiopika. В качестве сервера базы данных использовался Postgres. Для общения с базой данных использовалась
Tortoise ORM.

# Структура проекта

## backend

* `services` - python package со всем сервисами приложения
* `rpc_service` - вспомогательная библиотека на основе `aiopika` для шаблонизации описания сервисов
* `amqp_events` - вспомогательная библиотека для поддержки отправки событий через `rabbitmq`
* `game_model` - библиотека, реализующая всю логику игры "Сеги"

# Запуск

## Бэкенд

Проект имеет следующие зависимости:
* Брокер сообщений: Rabbitmq
* База данных: Postgres

Установите все необходимые зависимости проекта через следующую команду

```bash
pip install -r src/backend/requirements.txt
```

Перейдите в папку `src/backed` и запустите каждый микросервис в отдельном окне терминала через следующие команды (каждая команда соответствует запуску 1 микросервиса)

```
python -m services.accounts_service.main
python -m services.auth_service.main
python -m services.private_room_service.main
python -m services.searcher_service.main
python -m services.session_service.main
uvicorn services.gateway_service.main:app --host localhost --port 5000
```
