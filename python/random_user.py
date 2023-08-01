#!/usr/bin/python3
#
#
# == описание ==
# скрипт, который генерирует 5 случайнх пользователей (имя, фамилия и телефон),
# используя открытый API
#
# == алгоритм работы ==
#   1. с помощью пакета requests отправляем API-запрос
#   2. получаем ответ
#   3. преобразуем в JSON
#   4. получаем имя, фамилию, телефон
#   5. формируем строку с пользователем
#   6. делаем так 5 раз для генерации 5 пользователей
#
#
# == указания ==
#
# нужно поставить пакет requests:
#   > pip install requests
# либо поставить его через IDE
#


import requests


def print_random_user_info():
    response = requests.get('https://random-data-api.com/api/users/random_user')
    data = response.json()

    first_name = data['first_name']
    last_name = data['last_name']
    telephone = data['phone_number']

    print(f'{first_name} {last_name}, tel. {telephone}')


if __name__ == '__main__':
    for i in range(0, 5):
        print_random_user_info()
