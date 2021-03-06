# Advert

Веб-сервис, агрегатор объявлений. Используется Django 2.1 и Python 3.5

Основные компоненты:
* acomp - приложение, осуществляющее обработку асинхронных запросов (например, автозаполнение)
* api - приложение REST API
* article - приложение статей
* brand - приложение, осуществляющее работу с брендами
* geo - приложение, осуществляющее обработку геоданных
* lot - приложение по работе с торговыми предложениями (лотами)
* main - приложение, обеспечивающее некоторые основные функции сайта (главная страница, поиск и тд)
* media - медиа данные (фотографии объектов)
* parsers - парсеры, запускаемые вручную
* product - приложение, осуществляющее работу с каталогом продукции
* sender - приложение, осуществляющее отправку сообщений с форм
* static - изображения, CSS, JS
* supplier - приложение, осуществляющее работу с поставщиками
* templates - HTML шаблоны
* user - приложение, осуществляющее работу с пользователями (личный кабинет)
* utils - общие утилиты

## API

Документация к API

    http://your.domain/api/docs/

Swagger-схема находится в файле swagger.yaml

## Тестирование

Запуск unit-тестирования

    python manage.py test
