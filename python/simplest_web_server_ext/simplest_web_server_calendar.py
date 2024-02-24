import calendar
import datetime
import http
from http.server import BaseHTTPRequestHandler, HTTPServer

Handler = http.server.SimpleHTTPRequestHandler


class HelloWorldServer(BaseHTTPRequestHandler):
    def do_GET(self):
        # печатаем текущий месяц и сохраняем в строку
        today = datetime.datetime.today()
        month_calendar_str = calendar.month(today.year, today.month)

        # в HTML есть ряд особенностей вывода текста; обрабатываем их:
        # 1. переход на новую строку в HTML осуществляется не с помощью символа '\n',
        # а добавлением тега '<br>'
        month_calendar_str = month_calendar_str.replace('\n', '<br>')
        # 2. несколько пробелов подряд выводятся как один, потому вместо каждого
        # пробела ставим спец. символ, принудительно вставляющего пробел
        month_calendar_str = month_calendar_str.replace(' ', '&nbsp;')

        # добавляем в наш HTML-код страницы пункт, указывающий, какая кодировка
        # используется на странице:
        #   <meta charset="UTF-8">
        # это нужно, чтобы корректно отображались русские символы

        # еще один нюанс - используем тег '<tt>' (телетайп, то есть моноширинный шрифт),
        # чтобы наши строки не съезжали и все понедельники были друг под другом,
        # а субботы - под субботами

        html_page = \
            f"""
            <html>
                <head>
                    <title>Hello, World!</title>
                    <meta charset="UTF-8">
                </head>
                <body>
                    <h1 align='center'>Календарь</h1>
                    <tt>
                        {month_calendar_str}
                    </tt>
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
