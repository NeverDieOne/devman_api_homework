# Чат-бот Devman

Бот для запросов к Devman API о проверке домашнего задания.


## Как установить

1. `git clone https://github.com/NeverDieOne/devman_api_homework.git`
2. `cd devman_api_homework`
3. `python -m venv venv`
4. `. ./venv/bin/acitvate` (`venv/Scripts/Activate` on Windows)
5. `pip install -r requirements.txt`

## Переменные окружения

```.env
BOT_TOKEN=телеграм токен
DEV_TOKEN=токен авторизации Devman
CHAT_ID=id чата в телеграм
```

`CHAT_ID` можно узнать у специального бота `@userinfobot`.

## Пример использования

`python main.py`

## Пример запуска Docker

`docker run --env-file <path_to_env_file> neverdieone/devman_homework:latest`

## Цель проекта

Код написан в образовательных целях на онлайн-курсе для веб-разработчиков [Dvmn.org](https://dvmn.org/modules/)