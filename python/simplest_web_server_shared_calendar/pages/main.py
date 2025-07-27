from python.simplest_web_server_shared_calendar.pages import common


def main_page(server, users):
    page_content = \
        f"""
        <div align="center">
            <a href='/add_user'>Добавить</a>
        </div>
        <br>
        """

    page_content += '<div align="center">'
    for user in users:
        page_content += f"<a href='/{user['id']}'>{user['name']}</a><br>"
    page_content += \
        """
        </div>
        """

    html_page = common.compose_page('Календари', page_content)
    common.response_html(server, html_page)
