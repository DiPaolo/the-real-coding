import datetime
from http.server import BaseHTTPRequestHandler, HTTPServer

now = datetime.datetime.now() + datetime.timedelta(days=0)
today = datetime.datetime(now.year, now.month, now.day, 0, 0, 0)

EVENTS = [
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


def get_month_str(year: int, month: int) -> str:
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
                for event in EVENTS:
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

                out += f"      <td align='right' style='color: {color}; padding: 0px {padding_right}px 0px 0px; {border_style}'>{cur_day.day}{suffix}</td>"

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

    def show_main_page(self):
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
                    <h1 align='center'>Календарь</h1>
            """

        html_page += '<center><table>'

        cur_month = 1
        for i in range(0, 3):
            html_page += '<tr>'

            for j in range(0, 4):
                html_page += f"<td style='padding: 20px;'>{get_month_str(today.year, cur_month)}</td>"
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
