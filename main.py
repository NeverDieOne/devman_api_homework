import logging
import os
import time
from textwrap import dedent

import requests
import telegram
from dotenv import load_dotenv


logger = logging.getLogger('Devman Logger')


class LogsHandler(logging.Handler):
    def __init__(self, bot, chat_id, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.bot = bot
        self.chat_id = chat_id

    def emit(self, record):
        log_entry = self.format(record)
        self.bot.send_message(chat_id=self.chat_id, text=log_entry)


def main():
    load_dotenv()

    bot = telegram.Bot(token=os.environ['BOT_TOKEN'])
    chat_id = os.environ['CHAT_ID']

    logger.setLevel(logging.DEBUG)
    logger.addHandler(LogsHandler(bot, chat_id))
    logger.warning('Бот запущен!')

    while True:
        url = 'https://dvmn.org/api/long_polling/'
        headers = {
            'Authorization': f"Token {os.environ['DEV_TOKEN']}"
        }
        params = {}
        try:
            response = requests.get(url, headers=headers, params=params)
            response.raise_for_status()
            review = response.json()
            if review['status'] == 'found':
                params['timestamp'] = review['last_attempt_timestamp']

                new_attempt = review['new_attempts'][0]
                is_negative = new_attempt['is_negative']
                lesson_title = new_attempt['lesson_title']
                lesson_url = f'https://dvmn.org{new_attempt["lesson_url"]}'

                if is_negative:
                    message = f"""\
                    Работа "{lesson_title}" проверена.
                    К сожалению, в работе были найдены ошибки.
                    {lesson_url}
                    """
                else:
                    message = f"""\
                    Работа "{lesson_title}" проверена.
                    Преподавателю всё понравилось!
                    Можно приступать к следующему заданию!
                    {lesson_url}
                    """
                
                bot.send_message(
                    chat_id=chat_id,
                    text=dedent(message),
                    disable_web_page_preview=True
                )

            elif review['status'] == 'timeout':
                params['timestamp'] = review['timestamp_to_request']
        except requests.exceptions.ReadTimeout:
            pass
        except requests.exceptions.ConnectionError:
            time.sleep(60)
        except requests.exceptions.HTTPError:
            logger.exception('Something wrong with bot')


if __name__ == '__main__':
    main()
