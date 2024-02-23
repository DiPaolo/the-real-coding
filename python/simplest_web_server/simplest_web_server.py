import datetime
import http
from http.server import BaseHTTPRequestHandler, HTTPServer

Handler = http.server.SimpleHTTPRequestHandler


class HelloWorldServer(BaseHTTPRequestHandler):
    def do_GET(self):
        html_page = \
            f"""
            <html>
                <head>
                    <title>Hello, World!</title>
                </head>
                <body>
                    <h1 align='center'>Hello, World!</h1>
                    <h3 align='center'>{datetime.datetime.now()}</h3>
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
        print('Server crushed')

    webServer.server_close()
    print('Server stopped')
