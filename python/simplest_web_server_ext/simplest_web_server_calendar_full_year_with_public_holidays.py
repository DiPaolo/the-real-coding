import datetime
import http
from http.server import BaseHTTPRequestHandler, HTTPServer
from typing import List, Tuple

import requests

Handler = http.server.SimpleHTTPRequestHandler


def get_public_holidays(year: int) -> List[datetime.date]:
    out = list()

    res = requests.get(f'https://date.nager.at/api/v3/PublicHolidays/{year}/ru')
    if not res.ok:
        return out

    holiday_list_data = res.json()
    for holiday in holiday_list_data:
        date_str = holiday['date']
        date = datetime.datetime.strptime(date_str, '%Y-%m-%d')
        out.append(date.date())

    return out


TODAY = datetime.datetime.now()
PUBLIC_HOLIDAYS = get_public_holidays(TODAY.year)


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
    out = ''

    cur_day = datetime.datetime(year, month, 1)
    start_weekday = cur_day.weekday()

    month_names = ['Январь', 'Февраль', 'Март', 'Апрель', 'Май', 'Июнь', 'Июль',
                   'Август', 'Сентябрь', 'Октябрь', 'Ноябрь', 'Декабрь']

    out += '<table>'
    out += f'  <caption>{month_names[month - 1]}</caption>'
    out += '  <thead>'
    out += '    <tr>'

    for day in ['Пн', 'Вт', 'Ср', 'Чт', 'Пт', 'Сб', 'Вс']:
        out += f'    <th>{day}</th>'

    out += '    </tr>'
    out += '  </thead>'

    is_first_line = True
    days_in_month = get_days_in_month(year, month)
    done = False
    out += '  <tbody>'
    while not done:
        out += '    <tr>'
        for i in range(0, 7):
            if is_first_line and start_weekday != 0 and i < start_weekday:
                out += '      <td></td>'
            else:
                is_weekend_day = cur_day.weekday() in [5, 6]

                style = ''
                if is_weekend_day or cur_day.date() in PUBLIC_HOLIDAYS:
                    style += ' color: red;'
                if cur_day.date() == datetime.datetime.today().date():
                    style += ' border-style: double;'

                style_tag = f" style='{style}'" if style != '' else ''
                out += f"      <td align='right'{style_tag}>{cur_day.day}</td>"

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
                    <h1 align='center'>Календарь {TODAY.year}</h1>
            """

        html_page += '<center><table>'

        cur_month = 1
        for i in range(0, 3):
            html_page += '<tr>'

            for j in range(0, 4):
                html_page += f"<td style='padding: 20px; vertical-align: top;'>{get_month_str(TODAY.year, cur_month)}</td>"
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
