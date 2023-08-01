#!/usr/bin/python3
#
#
# == описание ==
# скрипт, который генерирует 5 случайнх пользователей (имя, фамилия и телефон + возраст),
# используя открытый API
#
# == алгоритм работы ==
#   1. с помощью пакета requests отправляем API-запрос
#   2. получаем ответ
#   3. преобразуем в JSON
#   4. получаем имя, фамилию, телефон, дату рождения
#   5. высчитываем возраст
#   6. формируем строку с пользователем
#   7. делаем так 5 раз для генерации 5 пользователей
#
#
# == указания ==
#
# нужно поставить пакет requests:
#   > pip install requests
# либо поставить его через IDE
#


import datetime

import requests


def get_age(date_of_birth):
    now = datetime.date.today()

    # получаем число полных лет
    years = now.year - date_of_birth.year

    # если день рождения еще не был в этом году, вычтем 1 год
    if date_of_birth.month > now.month:
        # если месяц дня рождения будет позже, то не имеет
        # смысл проверять дату
        years -= 1
    elif date_of_birth.month == now.month:
        if date_of_birth.day > now.day:
            years -= 1

    return years


def print_random_user_info():
    response = requests.get('https://random-data-api.com/api/users/random_user')
    data = response.json()

    first_name = data['first_name']
    last_name = data['last_name']
    telephone = data['phone_number']

    # день рождения в виде строки
    date_of_birth_str = data['date_of_birth']
    # зная формат даты, переводим в объект типа datetime
    date_of_birth = datetime.datetime.strptime(date_of_birth_str, '%Y-%m-%d')
    age = get_age(date_of_birth)

    print(f'{first_name} {last_name} ({age} y.o.), tel. {telephone}')


if __name__ == '__main__':
    for i in range(0, 5):
        print_random_user_info()
