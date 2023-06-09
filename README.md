## Описание:
Проект api_final_yatube это учебный проект выполненный студентом Яндекс практикумма. 

В проекте реализовано API для ресурса yatube, который позволяет пользователям создавать посты (в том числе содержащие изображения), комментарии к этм постам и подписки между пользователями.
Аутентификация пользователей происходит по JWT токену.

Используемые технологи перечмлены в файле requirements.txt:

## Установка на windows:

Клонировать репозиторий и перейти в него в командной строке:

```
git clone git@github.com:Temni23/api_final_yatube.git
```

```
cd api_final_yatube
```

Cоздать и активировать виртуальное окружение:

```
python -m venv venv
```

```
source venv/Scripts/activate
```

Установить зависимости из файла requirements.txt:

```
python -m pip install --upgrade pip
```

```
pip install -r requirements.txt
```

Выполнить миграции:

```
python manage.py migrate
```

Запустить проект:

```
python manage.py runserver
```

## Работа с проектом

После запуска проекта будут доступны следующие эндпоинты
```
http://127.0.0.1:8000/api/v1/posts/
```
```
http://127.0.0.1:8000/api/v1/groups/
```
```
http://127.0.0.1:8000/api/v1/follow/
```

В папке /yatube_api/static/ находится файл redoc.yaml с докментацией по данному проекту.  [Прочитать файл можно по этой ссылке](https://redocly.github.io/redoc/)
