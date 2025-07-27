import datetime
import random
import re
import string
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs

from python.simplest_web_server_shared_calendar.pages import main, users, slots

now = datetime.datetime.now() + datetime.timedelta(days=0)
today = datetime.datetime(now.year, now.month, now.day, 0, 0, 0)

USERS = [
    {
        'name': 'DiPaolo',
        'id': '5hb4b2ce',
        'events': [
            # tomorrow
            {
                'datetime': today + datetime.timedelta(hours=9),
                'title': 'встреча в 09:00'
            },
            {
                'datetime': today + datetime.timedelta(hours=10),
                'title': 'встреча в 10:00'
            },
            {
                'datetime': today + datetime.timedelta(hours=11),
                'title': 'встреча в 11:00'
            },
            {
                'datetime': today + datetime.timedelta(hours=12),
                'title': 'встреча в 12:00'
            },
            {
                'datetime': today + datetime.timedelta(hours=13),
                'title': 'встреча в 13:00'
            },
            {
                'datetime': today + datetime.timedelta(hours=14),
                'title': 'встреча в 14:00'
            },
            {
                'datetime': today + datetime.timedelta(hours=15),
                'title': 'встреча в 15:00'
            },
            {
                'datetime': today + datetime.timedelta(hours=16),
                'title': 'встреча в 16:00'
            },
            {
                'datetime': today + datetime.timedelta(hours=17),
                'title': 'встреча в 17:00'
            },
            # the day after tomorrow
            {
                'datetime': today + datetime.timedelta(days=1, hours=12),
                'title': 'встреча в 12:00'
            },
            {
                'datetime': today + datetime.timedelta(days=1, hours=17),
                'title': 'встреча в 17:00'
            },
            # 2 days later
            {
                'datetime': today + datetime.timedelta(days=2, hours=14),
                'title': 'встреча в 14:00'
            },
            # in a week
            {
                'datetime': today + datetime.timedelta(days=7, hours=11),
                'title': 'встреча в 11:00'
            }
        ]
    },
    {
        'name': 'Joshua',
        'id': '88jl3hsn',
        'events': [
            # yesterday
            {
                'datetime': today + datetime.timedelta(days=-1, hours=13),
                'title': 'встреча в 13:00'
            },
            # today
            {
                'datetime': today + datetime.timedelta(hours=9),
                'title': 'встреча в 09:00'
            },
            # tomorrow
            {
                'datetime': today + datetime.timedelta(hours=9),
                'title': 'встреча в 09:00'
            },
            {
                'datetime': today + datetime.timedelta(hours=10),
                'title': 'встреча в 10:00'
            },
            {
                'datetime': today + datetime.timedelta(hours=11),
                'title': 'встреча в 11:00'
            },
            {
                'datetime': today + datetime.timedelta(hours=12),
                'title': 'встреча в 12:00'
            },
            {
                'datetime': today + datetime.timedelta(hours=13),
                'title': 'встреча в 13:00'
            },
            {
                'datetime': today + datetime.timedelta(hours=14),
                'title': 'встреча в 14:00'
            },
            {
                'datetime': today + datetime.timedelta(hours=15),
                'title': 'встреча в 15:00'
            },
            {
                'datetime': today + datetime.timedelta(hours=16),
                'title': 'встреча в 16:00'
            },
            {
                'datetime': today + datetime.timedelta(hours=17),
                'title': 'встреча в 17:00'
            },
            # 2 days later
            {
                'datetime': today + datetime.timedelta(days=2, hours=14),
                'title': 'встреча в 14:00'
            },
            # in a month+
            {
                'datetime': today + datetime.timedelta(days=37, hours=11),
                'title': 'встреча в 11:00'
            }
        ]
    }
]


def add_user(name: str) -> str:
    user_id = ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(0, 8))
    USERS.append({
        'name': name,
        'id': user_id,
        'events': []
    })

    return user_id


def book_slot(user_id: str, year: int, month: int, day: int, hour: int, title: str):
    for user in USERS:
        if user['id'] == user_id:
            user['events'].append({
                'datetime': datetime.datetime(year, month, day, hour),
                'title': title
            })
            break


class HelloWorldServer(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed_path = urlparse(self.path)
        if parsed_path.path == '/':
            self.show_main_page()
        elif parsed_path.path == '/add_user':
            if parsed_path.query == '':
                self.show_add_user_page()
            else:
                queries = parse_qs(parsed_path.query)
                if 'name' in queries:
                    user_id = add_user(queries['name'][0])
                    self.show_user_main_page(user_id)
        else:
            res = re.match(r'^\/([\w|\d]{8})$', parsed_path.path)
            if res is not None and len(res.groups()) == 1:
                user_id = res.groups()[0]
                self.show_user_main_page(user_id)
            else:
                res = re.match(r'^\/([\w|\d]{8})\/(\d+)\/(\d+)\/(\d+)$', parsed_path.path)
                if res is not None and len(res.groups()) == 4:
                    user_id = res.groups()[0]
                    year = int(res.groups()[1])
                    month = int(res.groups()[2])
                    day = int(res.groups()[3])
                    self.show_date_page(user_id, year, month, day)
                else:
                    res = re.match(r'^\/([\w|\d]{8})\/(\d+)\/(\d+)\/(\d+)\/(\d+)\/book$', parsed_path.path)
                    if res is not None and len(res.groups()) == 5:
                        user_id = res.groups()[0]
                        year = int(res.groups()[1])
                        month = int(res.groups()[2])
                        day = int(res.groups()[3])
                        hour = int(res.groups()[4])

                        if parsed_path.query == '':
                            self.show_book_slot_page(user_id, year, month, day, hour)
                        else:
                            queries = parse_qs(parsed_path.query)
                            if 'title' in queries:
                                book_slot(user_id, year, month, day, hour, queries['title'][0])
                                self.show_date_page(user_id, year, month, day)

    def show_main_page(self):
        main.main_page(self, USERS)

    def show_user_main_page(self, user_id: str):
        users.main_page(self, USERS, user_id)

    def show_add_user_page(self):
        users.add_user_page(self)

    def show_date_page(self, user_id: str, year: int, month: int, day: int):
        slots.date_page(self, USERS, user_id, year, month, day)

    def show_book_slot_page(self, user_id: str, year: int, month: int, day: int, hour: int):
        slots.book_slot_page(self, USERS, user_id, year, month, day, hour)


if __name__ == "__main__":
    webServer = HTTPServer(server_address=('127.0.0.1', 8080),
                           RequestHandlerClass=HelloWorldServer)
    print('Server started')

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass
    except Exception as ex:
        print(f'Server unexpectedly finished ({ex})')

    webServer.server_close()
    print('Server stopped')
