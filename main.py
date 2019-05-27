import requests
import os
import telegram
from dotenv import load_dotenv
import logging


def main():
    load_dotenv()

    bot = telegram.Bot(token=os.environ['BOT_TOKEN'])
    chat_id = os.environ['CHAT_ID']

    class MyLogsHandler(logging.Handler):

        def __init__(self, bot, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.bot = bot

        def emit(self, record):
            log_entry = self.format(record)
            self.bot.send_message(chat_id=os.environ['CHAT_ID'],
                                  text=log_entry)

    logger = logging.getLogger('Devman Logger')
    logger.setLevel(logging.DEBUG)
    logger.addHandler(MyLogsHandler(bot))
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
            response_json = response.json()
            if response_json['status'] == 'found':
                params['timestamp'] = response_json['last_attempt_timestamp']

                new_attempt = response_json['new_attempts'][0]
                is_negative = new_attempt['is_negative']
                lesson_title = new_attempt['lesson_title']
                lesson_url = f'https://dvmn.org{new_attempt["lesson_url"]}'

                if is_negative:
                    bot.send_message(chat_id=chat_id,
                                     text=f'Работа "{lesson_title}" проверена.\n'
                                     f'К сожалению, в работе были найдены ошибки.\n{lesson_url}')
                else:
                    bot.send_message(chat_id=chat_id,
                                     text=f'Работа "{lesson_title}" проверена.\nПреподавателю всё понравилось!'
                                     f' Можно приступать к следующему заданию!\n{lesson_url}')

            elif response_json['status'] == 'timeout':
                params['timestamp'] = response_json['timestamp_to_request']
        except (requests.exceptions.ReadTimeout, requests.exceptions.ConnectionError) as error:
            logger.warning(f"Бот упал с ошибкой: {error}")
            continue


if __name__ == '__main__':
    main()
