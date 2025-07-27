import datetime

from python.simplest_web_server_shared_calendar.pages import common
from python.simplest_web_server_shared_calendar.simplest_web_server_shared_calendar import USERS

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


def get_month_str(users, user_id: str, year: int, month: int) -> str:
    events = list()
    for user in users:
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


def main_page(server, users, user_id: str):
    user_name = ''
    for user in users:
        if user['id'] == user_id:
            user_name = user['name']
            break

    today = datetime.datetime.today()

    page_content = \
        f"""
            <table>
        """

    cur_month = 1
    for i in range(0, 3):
        page_content += '<tr>'

        for j in range(0, 4):
            page_content += f"<td style='padding: 20px;'>{get_month_str(USERS, user_id, today.year, cur_month)}</td>"
            cur_month += 1

        page_content += '</tr>'

    page_content += \
        """
            </table>
        """

    html_page = common.compose_page(f'Календарь({user_name})', page_content)
    common.response_html(server, html_page)


def add_user_page(server):
    page_content = \
        """
        <form>
            <label for="title">Имя:</label><input type="text" id="name" name="name"><br>
            <input type="submit" value="Добавить">
        </form>
        """

    page_content = common.compose_page(f'Добавить пользователя', page_content)
    common.response_html(server, page_content)
