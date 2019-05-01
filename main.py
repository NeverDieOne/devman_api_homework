import requests
import os
import telegram
from dotenv import load_dotenv

load_dotenv()


def main():
    chat_id = os.getenv('CHAT_ID')
    bot = telegram.Bot(token=os.getenv('BOT_TOKEN'))

    while True:
        url = 'https://dvmn.org/api/long_polling/'
        headers = {
            'Authorization': f"Token {os.getenv('DEV_TOKEN')}"
        }
        params = {}
        try:
            response = requests.get(url, headers=headers, params=params).json()
            if response['status'] == 'found':
                params['timestamp'] = response['last_attempt_timestamp']

                new_attempt = response['new_attempts'][0]
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

            elif response['status'] == 'timeout':
                params['timestamp'] = response['timestamp_to_request']
        except requests.exceptions.ReadTimeout:
            continue


if __name__ == '__main__':
    main()
