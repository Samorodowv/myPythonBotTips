import requests
from xml.etree import ElementTree
import os
import datetime

# Todo Дописать кастомные праздники день программиста/бухгалтера/системного администратора/ молочной промышленности
# Todo выполнение кода в отведённое для этого время

proxy = 'http://040938:0508Asdf5466@192.168.168.40:3128'
os.environ['http_proxy'] = proxy
os.environ['HTTP_PROXY'] = proxy
os.environ['https_proxy'] = proxy
os.environ['HTTPS_PROXY'] = proxy


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
    print(str_day)
    for days in calendar.iter('days'):
        for day in days:
            if day.attrib.get('d') == str_day:
                return day.attrib.get('t') == '1'
    if date.weekday() == 6 or date.weekday() == 5:
        return True
    return False


if __name__ == '__main__':
    print(verify_dayoff())
    print(verify_holiday())

