from python.simplest_web_server_shared_calendar.pages import common


def date_page(server, users, user_id: str, year: int, month: int, day: int):
    user_name = ''
    events = list()
    for user in users:
        if user['id'] == user_id:
            user_name = user['name']
            events = user['events']
            break

    page_content = \
        f"""
            <table>
        """

    today_events = list()
    for ev in events:
        if ev['datetime'].year == year and ev['datetime'].month == month and ev['datetime'].day == day:
            today_events.append(ev)

    for i in range(9, 18):
        event_name = ''
        for ev in today_events:
            if ev['datetime'].hour == i:
                event_name = ev['title']

        page_content += \
            """
            <tr>
                <td>
            """

        if event_name == '':
            page_content += f"<a href='/{user_id}/{year:04}/{month:02}/{day:02}/{i:02}/book'>"

        page_content += f'{i:02}:00-{i + 1:02}:00'

        if event_name == '':
            page_content += '</a>'

        page_content += \
            f"""
                </td>
                <td>{event_name}</td>
            </tr>
            """

    page_content += \
        """
            </table>
        """

    html_page = common.compose_page(f'{day:02}.{month:02}.{year:04} ({user_name})', page_content,
                                    [(f'/{user_id}', f'Календарь {user_name}')])
    common.response_html(server, html_page)


def book_slot_page(server, users, user_id: str, year: int, month: int, day: int, hour: int):
    user_name = ''
    for user in users:
        if user['id'] == user_id:
            user_name = user['name']
            break

    page_content = \
        f"""
            <p align='center'><b>Дата</b>: {day:02}.{month:02}.{year:04}
            <p align='center'><b>Время</b>: {hour:02}:00-{hour + 1:02}:00
            <form>
                <label for="title">Название:</label><input class='uk-input' type="text" id="title" name="title"><br>
                <input type="submit" value="Добавить">
            </form>
        """

    html_page = common.compose_page(f'Добавить событие ({user_name})', page_content,
                                    [(f'/{user_id}', f'Календарь {user_name}')])
    common.response_html(server, html_page)
