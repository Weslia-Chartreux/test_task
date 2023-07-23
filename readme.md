# RESTful API для приложения социальной сети

Простой RESTful API с помощью FastAPI для приложения социальной сети. В этом проекте реализована авторизация с помощью jwt. 

## Регистрация и авторизация

С помощью запроса POST /api/signup/ регистрируется аккаунт с запросом {'name': '', 'password': ''}. После этого с помощью запроса POST /api/login/ {'name': '', 'password': ''} получаем временный токен для работы с API.

## Работа с постами

Открывается возможность создавать (POST) и изменять (PATCH) посты /api/post/{post_id} (изменять посты может только автор). Пример запроса с POST {'title': '', 'content':''}, также нужно в заголовке указать временный токен {'accept': 'application/json', 'Authorization': 'Bearer {token}'}.

Без авторизации можно использовать запрос GET:
1. По id записи /api/post/{post_id} (без body)
2. Получение всех записей /api/post/ (без body)

Также реализован запрос DELETE /api/post/{post_id} (без body и с авторизацией) (удалять посты может только автор).

## Система лайков

Реализована система лайков. Для "лайка" публикации нужно отправить запрос POST /post/like/{row_id} (без body и с авторизацией). Один пользователь может поставить только один лайк.

Можно убрать лайк с публикации, для этого нужно отправить запрос DELETE /post/like/{row_id} (без body и с авторизацией).

## Пример использования API

python
import requests

url = 'http://127.0.0.1:8000/signup'
headers = {'accept': 'application/json', 'Content-Type': 'application/json'}
data = {'username': 'flyingsponge', 'password': 'SpongePassword'}

response = requests.post(url, headers=headers, json=data)

print(response.status_code) # Вывод кода статуса ответа сервера
print(response.json()) # Вывод тела ответа в формате JSON


## Запуск проекта

Для запуска проекта необходимо выполнить следующие шаги:

1. Установить зависимости из файла requirements.txt.
2. Запустить сервер запуском main.py (или командой uvicorn main:app.)
3. Открыть документацию API по адресу http://127.0.0.1:8000/docs.