import schedule
import time
import requests
from xml.etree import ElementTree
import datetime

# Todo Дописать кастомные праздники день программиста/бухгалтера/системного администратора/ молочной промышленности

# если сегодня праздник и вчера не было праздника, говорим что сегодня праздник, вызовем в 9.00
def verify_holiday():
    today = datetime.datetime.today()
    yesterday = today - datetime.timedelta(days=1)
    response = requests.get(f"http://xmlcalendar.ru/data/ru/{today.strftime('%Y')}/calendar.xml")
    calendar = ElementTree.fromstring(response.content)
    today_holiday = check_holiday(today, calendar)
    yesterday_holiday = check_holiday(yesterday, calendar)
    return f" Уважаемые коллеги, поздравляю с праздником! \n Сегодня : {today_holiday}" \
        if (today_holiday != "" and yesterday_holiday == "") else None


# если сегодня не выходной а завтра выходной, пожелаем хороших выходных, выполним в 17:00
def verify_dayoff():
    today = datetime.datetime.today()
    tomorrow = today + datetime.timedelta(days=1)
    response = requests.get(f"http://xmlcalendar.ru/data/ru/{today.strftime('%Y')}/calendar.xml")
    calendar = ElementTree.fromstring(response.content)
    return f" Уважаемые коллеги, желаю Вам хороших выходных!" if (
            not check_day_off(today, calendar) and check_day_off(tomorrow, calendar)) else None


# проверка что сегодня праздник
def check_holiday(date: datetime.datetime, calendar) -> str:
    str_day = date.strftime('%m.%d')
    for days in calendar.iter('days'):
        for day in days:
            if day.attrib.get('d') == str_day and day.attrib.get('h') is not None:
                for holidays in calendar.iter('holidays'):
                    for holiday in holidays:
                        if holiday.attrib.get('id') == day.attrib.get('h'):
                            return holiday.attrib.get('title')
    return ""


# true если выходной или суббота/воскресенье
def check_day_off(date: datetime.datetime, calendar) -> bool:
    str_day = date.strftime('%m.%d')
    for days in calendar.iter('days'):
        for day in days:
            if day.attrib.get('d') == str_day:
                return day.attrib.get('t') == '1'
    if date.weekday() == 6 or date.weekday() == 5:
        return True
    return False


def say_at_morning():
    print(verify_holiday())


def say_at_end_of_the_day():
    print(verify_dayoff())


schedule.every().day.at("09:00").do(say_at_morning)
schedule.every().day.at("16:55").do(say_at_end_of_the_day)


def schedule_loop():
    while True:
        schedule.run_pending()
        time.sleep(1)


schedule_loop()


