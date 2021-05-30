# Сайт _Куда пойти - Москва глазами Артема_

Этот сайт позволяет аналогично сайту Яндекс.Афиша найти на карте Москвы интересные
места для досуга и отдыха.

![intro](.gitbook/assets/intro4.gif)

Проект создан в учебных целях в рамках курса [Devman Django](https://dvmn.org/modules/django/lesson/yandex-afisha/)

[Проверить сайт можно тут](https://rushen.pythonanywhere.com/)

[Административная панель сайта](https://rushen.pythonanywhere.com/admin/)

## Разворачивание проекта для разработки локально

При разработке был использован python v3.8

### С использованием стандартных средст python

* Скачать репозиторий проекта и перейти в его директорию
```shell script
git clone https://github.com/realrushen/devman-django.git && cd ./devman-django
```
* Инициализировать и активировать виртуальное окружение
```shell script
python3 -m venv .venv && source .venv/bin/activate
```

* Установить зависимости
```shell script
pip3 install -r requirements.txt
```

* Задать настройки приложения из переменных окружения
```shell script
# может быть любой рандомно сгенерированной строкой
export SECRET_KEY='django-insecure-9bu(j)x@32x&e&0(gq*eto^=(+fqa%ith+se#1k40#%^)t&l5c'
# путь к настройкам для разработки
export DJANGO_SETTINGS_MODULE='where_to_go.settings.development'
```
* Применить миграции бызы данных
```shell script
python3 manage.py migrate
```
* Запустить development сервер Django
```shell script
python3 manage.py runserver
```

* Перейти на http://127.0.0.1:8000/

### С использованием [poetry](https://github.com/python-poetry/poetry) (рекомендовано)

* Установить `poetry` по [инструкции](https://python-poetry.org/docs/#installation)

* Скачать репозиторий проекта и перейти в его директорию
```shell script
git clone https://github.com/realrushen/devman-django.git && cd ./devman-django
```

* Инициализировать development окружение
```shell script
poetry install
```

* Задать настройки приложения из переменных окружения
```shell script
# может быть любой рандомно сгенерированной строкой
export SECRET_KEY='django-insecure-9bu(j)x@32x&e&0(gq*eto^=(+fqa%ith+se#1k40#%^)t&l5c'
# путь к настройкам для разработки
export DJANGO_SETTINGS_MODULE='where_to_go.settings.development'
```

* Применить миграции бызы данных
```shell script
python3 manage.py migrate
```
* Запустить development сервер Django
```shell script
python3 manage.py runserver
```

* Перейти на http://127.0.0.1:8000/

## Наполнение сайта данными
Предусмотренно два способа загрузки данных в проект:
1. В ручном режиме зерез [админ панель](https://rushen.pythonanywhere.com/admin/)
2. С помошью кастомной менеджмент команды Django `python3 manage.py load_place`.
Подробная информация: `python3 manage.py load_place -h`

[Структура данных для автоматической загрузки](https://github.com/realrushen/devman-django/blob/master/.gitbook/data/example.json)

## Лицензирование и авторские права

Данные взяты с https://kudago.com/

