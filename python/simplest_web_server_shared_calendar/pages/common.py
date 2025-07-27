from typing import List, Tuple


def compose_page(title: str, content: str, page_specific_links: List[Tuple[str, str]] = None) -> str:
    if page_specific_links is None:
        page_specific_links = list()

    page_specific_links.insert(0, ('/', 'Главная'))

    return \
            f"""
        <html>
            <!-- UIkit CSS -->
            <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/uikit@3.22.4/dist/css/uikit.min.css" />
            
            <!-- UIkit JS -->
            <script src="https://cdn.jsdelivr.net/npm/uikit@3.22.4/dist/js/uikit.min.js"></script>
            <script src="https://cdn.jsdelivr.net/npm/uikit@3.22.4/dist/js/uikit-icons.min.js"></script>
            <head>
                <title>Hello, World!</title>
                <meta charset="UTF-8">
            </head>
            <body>
        """ \
            + \
            '\n'.join([f"<p><a href='{l[0]}'>{l[1]}</a></p>" for l in page_specific_links]) \
            + \
            f"""
                <h1 align='center'>{title}</h1>
                <div style='width: 60%; margin-left: auto; margin-right: auto;'>
                    {content}
                </div>
            </body>
        </html>
        """


def response_html(server, html: str):
    body = html.encode('UTF-8', 'replace')

    server.send_response(200)
    server.send_header("Content-type", "text/html")
    server.send_header('Content-Length', str(len(body)))
    server.end_headers()

    server.wfile.write(body)
