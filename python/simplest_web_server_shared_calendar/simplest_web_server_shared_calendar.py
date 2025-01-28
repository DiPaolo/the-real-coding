import datetime
import random
import re
import string
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs

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

# every hour 9-18
SLOTS_IN_DAY = 9


def get_days_in_month(year, month):
    if month == 2:
        if year % 4 == 0 or year % 100 == 0 and year % 400 == 0:
            return 29
        else:
            return 28
    elif month in [1, 3, 5, 7, 8, 10, 12]:
        return 31
    else:
        return 30

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


def get_month_str(user_id: str, year: int, month: int) -> str:
    events = list()
    for user in USERS:
        if user['id'] == user_id:
            events = user['events']

    today = datetime.datetime.today()
    out = ''

    cur_day = datetime.datetime(year, month, 1, hour=0, minute=0, second=0)
    start_weekday = cur_day.weekday()

    month_names = ['Январь', 'Февраль', 'Март', 'Апрель', 'Май', 'Июнь', 'Июль',
                   'Август', 'Сентябрь', 'Октябрь', 'Ноябрь', 'Декабрь']

    out += '<table>'
    out += f'  <caption>{month_names[month - 1]} {year}</caption>'
    out += '  <thead>'
    out += '    <tr>'

    for day in ['Пн', 'Вт', 'Ср', 'Чт', 'Пт', 'Сб', 'Вс']:
        out += f"    <th style='width: 28px;'>{day}</th>"

    out += '    </tr>'
    out += '  </thead>'

    is_first_line = True
    days_in_month = get_days_in_month(year, month)
    done = False
    out += '  <tbody>'
    while not done:
        out += "    <tr style='height: 30px'>"
        for i in range(0, 7):
            if is_first_line and start_weekday != 0 and i < start_weekday:
                out += '      <td></td>'
            else:
                # get count of free slots for this day
                free_slots = SLOTS_IN_DAY
                for event in events:
                    if event['datetime'].year == cur_day.year and \
                            event['datetime'].month == cur_day.month and \
                            event['datetime'].day == cur_day.day:
                        free_slots -= 1

                is_weekend_day = cur_day.weekday() in [5, 6]

                color = ''
                suffix = ''
                padding_right = 10 if free_slots == SLOTS_IN_DAY else 4

                if cur_day < today:
                    color = 'lightgrey'
                else:
                    if free_slots == 0:
                        color = 'lightpink' if is_weekend_day else 'lightgrey'
                    else:
                        color = 'red' if is_weekend_day else 'black'
                        if free_slots != SLOTS_IN_DAY:
                            suffix = f"<sup style='font-size: 12px;'>{free_slots}</sup>"

                border_style = ''
                if cur_day.date() == datetime.datetime.today().date():
                    border_style = 'border-style: double;'
                    padding_right = 6

                style = f'color: {color}; padding: 0px {padding_right}px 0px 0px; {border_style}'
                out += f"<td align='right' style='{style}'>"
                if cur_day >= today and free_slots > 0:
                    out += f"<a href='/{user_id}/{cur_day.year:04}/{cur_day.month:02}/{cur_day.day:02}'>"
                out += f'{cur_day.day}{suffix}'
                if cur_day >= today and free_slots > 0:
                    out += '</a>'
                out += '</td>'

                if cur_day.day == days_in_month:
                    done = True
                    break
                else:
                    cur_day += datetime.timedelta(days=1)

        is_first_line = False
        out += '    </tr>'

    out += '  </tbody>'
    out += '</table>'

    return out


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
        html_page = \
            f"""
            <html>
                <head>
                    <title>Hello, World!</title>
                    <meta charset="UTF-8">
                </head>
                <body>
                    <h1 align='center'>Календари</h1>
            """

        html_page += \
            f"""
            <div align="center">
                <a href='/add_user'>Добавить</a>
            </div>
            <br>
            """
        html_page += '<div align="center">'

        for user in USERS:
            html_page += f"<a href='/{user['id']}'>{user['name']}</a><br>"

        html_page += \
            """
                    </div>
                </body>
            </html>
            """

        body = html_page.encode('UTF-8', 'replace')

        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.send_header('Content-Length', str(len(body)))
        self.end_headers()

        self.wfile.write(body)

    def show_user_main_page(self, user_id: str):
        user_name = ''
        for user in USERS:
            if user['id'] == user_id:
                user_name = user['name']
                break

        today = datetime.datetime.today()

        # добавляем в наш HTML-код страницы пункт, указывающий, какая кодировка
        # используется на странице:
        #   <meta charset="UTF-8">
        # это нужно, чтобы корректно отображались русские символы

        html_page = ''

        html_page += \
            f"""
            <html>
                <head>
                    <title>Hello, World!</title>
                    <meta charset="UTF-8">
                </head>
                <body>
                    <h1 align='center'>Календарь ({user_name})</h1>
            """

        html_page += '<center><table>'

        cur_month = 1
        for i in range(0, 3):
            html_page += '<tr>'

            for j in range(0, 4):
                html_page += f"<td style='padding: 20px;'>{get_month_str(user_id, today.year, cur_month)}</td>"
                cur_month += 1

            html_page += '</tr>'

        html_page += \
            """

                        </table>
                    </center>
                </body>
            </html>
            """

        body = html_page.encode('UTF-8', 'replace')

        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.send_header('Content-Length', str(len(body)))
        self.end_headers()

        self.wfile.write(body)

    def show_add_user_page(self):
        html_page = ''

        html_page += \
            f"""
            <html>
                <head>
                    <title>Hello, World!</title>
                    <meta charset="UTF-8">
                </head>
                <body>
                    <p><a href='/'>Главная</a></p>
                    <h1 align='center'>Добавить пользователя</h1>
            """

        html_page += \
            """
            <center>
                <form>
                    <label for="title">Имя:</label><input type="text" id="name" name="name"><br>
                    <input type="submit" value="Добавить">
            """

        html_page += \
            """

                        </form>
                    </center>
                </body>
            </html>
            """

        body = html_page.encode('UTF-8', 'replace')

        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.send_header('Content-Length', str(len(body)))
        self.end_headers()

        self.wfile.write(body)

    def show_date_page(self, user_id: str, year: int, month: int, day: int):
        user_name = ''
        events = list()
        for user in USERS:
            if user['id'] == user_id:
                user_name = user['name']
                events = user['events']
                break

        html_page = ''

        html_page += \
            f"""
            <html>
                <head>
                    <title>Hello, World!</title>
                    <meta charset="UTF-8">
                </head>
                <body>
                    <p><a href='/'>Главная</a></p>
                    <p><a href='/{user_id}'>Календарь {user_name}</a></p>
                    <h1 align='center'>{day:02}.{month:02}.{year:04} ({user_name})</h1>
            """

        html_page += '<center><table>'

        today_events = list()
        for ev in events:
            if ev['datetime'].year == year and ev['datetime'].month == month and ev['datetime'].day == day:
                today_events.append(ev)

        for i in range(9, 18):
            event_name = ''
            for ev in today_events:
                if ev['datetime'].hour == i:
                    event_name = ev['title']

            html_page += \
                """
                <tr>
                    <td>
                """

            if event_name == '':
                html_page += f"<a href='/{user_id}/{year:04}/{month:02}/{day:02}/{i:02}/book'>"

            html_page += f'{i:02}:00-{i + 1:02}:00'

            if event_name == '':
                html_page += '</a>'

            html_page += \
                f"""
                    </td>
                    <td>{event_name}</td>
                </tr>
                """

        html_page += \
            """

                        </table>
                    </center>
                </body>
            </html>
            """

        body = html_page.encode('UTF-8', 'replace')

        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.send_header('Content-Length', str(len(body)))
        self.end_headers()

        self.wfile.write(body)

    def show_book_slot_page(self, user_id: str, year: int, month: int, day: int, hour: int):
        user_name = ''
        for user in USERS:
            if user['id'] == user_id:
                user_name = user['name']
                break

        html_page = ''

        html_page += \
            f"""
            <html>
                <head>
                    <title>Hello, World!</title>
                    <meta charset="UTF-8">
                </head>
                <body>
                    <p><a href='/'>Главная</a></p>
                    <p><a href='/{user_id}'>Календарь {user_name}</a></p>
                    <h1 align='center'>Добавить событие ({user_name})</h1>
                    <p align='center'><b>Дата</b>: {day:02}.{month:02}.{year:04}
                    <p align='center'><b>Время</b>: {hour:02}:00-{hour + 1:02}:00
            """

        html_page += \
            """
            <center>
                <form>
                    <label for="title">Название:</label><input type="text" id="title" name="title"><br>
                    <input type="submit" value="Добавить">
            """

        html_page += \
            """

                        </form>
                    </center>
                </body>
            </html>
            """

        body = html_page.encode('UTF-8', 'replace')

        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.send_header('Content-Length', str(len(body)))
        self.end_headers()

        self.wfile.write(body)


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
