import requests
from dotenv import load_dotenv
import os
load_dotenv()


def main():
    while True:
        url = 'https://dvmn.org/api/long_polling/'
        headers = {
            'Authorization': f"Token {os.getenv('TOKEN')}"
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

                print(is_negative, lesson_title, lesson_url)

            elif response['status'] == 'timeout':
                params['timestamp'] = response['timestamp_to_request']
        except requests.exceptions.ReadTimeout:
            continue


if __name__ == '__main__':
    main()
