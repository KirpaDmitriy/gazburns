# Gazburnы

## Описание
Представленное решение предоставляет API для генерации и созания слоганов маркетинговых изображений для приложений Газпромбанка.

API построено на базе FastAPI и который предоставляет ручки для [генерации изображения](./handlers/images.py) по описанию кластера пользователя, [добавления текста](./handlers/images.py) на изображение, !!! перегенерации изображения !!!, [получения истории](./handlers/history.py) работы пользователя с генерациями, [получения изображения с файловой системы](./handlers/files_server.py) сервера, а также стандартные ручки [авторизации](./handlers/access.py). Сгенерированные изображения представляются в виде ссылок. Изображение при генерации сохраняются на ФС сервера, откуда пользователь может их скачать.

Генерация изображений [основана](./src/images_generation.py) на открытой модели Kandinsky. Её задача - сгенерировать объекты для наполнения изображения (символизирующие отпуск чемоданы, люксовые яхты и автомобили, демонстрирующие город и банк мультяшные фигурки). Этот объект вырезается и встраивается в сгенерированный фон. По желанию к изображению можно добавить текст.

## Общая структура репозитория
- [main.py](./main.py) - файл с приложением API
- [models.py](./models.py) - файл с моделями используемых данных
- [handlers](./handlers) - модуль с ручками
- [src](./src) - модуль с ML- и вспомогательными утилитами
- [database](./database) - модуль с моделями и методами для БД

## Стек
- FastAPI - для веб-приложения
- Pydantic - для валидации моделей
- asyncpg - для асинхронного взаимодействия с базой
- jose - для авторизации пользователя с помощью jwt-токенов
- diffusers - для генерации изображений по текстовому описанию
- rembg - для удаления фона изображения


## Запуск
Для запуска нужно:
1) Установить все зависимости из [requirements.txt](./requirements.txt)
2) Установить PostgreSQL с помощью [скрипта](./database/scripts/create_db.sh)
3) Создать базу и таблицы с помощью [скриптов](./database/scripts/SQL)
4) Запустить приложение [start.sh](./start.sh)

Для работы нейросетевой модели требуется GPU.
