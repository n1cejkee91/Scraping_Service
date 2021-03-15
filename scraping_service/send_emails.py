import os
import sys
import datetime
import django
from django.contrib.auth import get_user_model
from django.core.mail import EmailMultiAlternatives

proj = os.path.dirname(os.path.abspath('manage.py'))
sys.path.append(proj)
os.environ["DJANGO_SETTINGS_MODULE"] = "scraping_service.settings"

django.setup()
from scraping.models import Vacancy, Errors, Url
from scraping_service.settings import EMAIL_HOST_USER

ADMIN_USER = EMAIL_HOST_USER

today = datetime.date.today()

empty = '<h2>К сожалению по Вашему запросу ничего не найдено!<h2>'

subject = f'Рассылка вакансий за {today}'
text_content = 'Рассылка вакансий'
from_email = EMAIL_HOST_USER

User = get_user_model()
qs = User.objects.filter(send_email=True).values('city', 'language', 'email')
users_dct = {}

for i in qs:
    users_dct.setdefault((i['city'], i['language']), [])
    users_dct[(i['city'], i['language'])].append(i['email'])  # Ключ это пара id (город и ЯП), значение email'ов
if users_dct:
    params = {'city_id__in': [], 'language_id__in': []}
    for pair in users_dct.keys():
        params['city_id__in'].append(pair[0])
        params['language_id__in'].append(pair[1])  # Значения по городам и ЯП, которые необходимо получить из БД
    qs = Vacancy.objects.filter(**params, timestamp=today).values()[:10]
    vacancies = {}
    for i in qs:
        vacancies.setdefault((i['city_id'], i['language_id']), [])
        vacancies[(i['city_id'], i['language_id'])].append(i)
    for keys, emails in users_dct.items():
        rows = vacancies.get(keys, [])
        html = ''
        for row in rows:
            html += f'<h2><a href="{row["url"]}">{row["title"]}</a></h2>'
            html += f'<p>{row["description"]}</p>'
            html += f'<p>{row["company"]}</p><br><hr>'
        _html = html if html else empty
        for email in emails:
            to = email
            msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
            msg.attach_alternative(_html, "text/html")
            msg.send()


qs = Errors.objects.filter(timestamp=today)
subject = ''
text_content = ''
to = ADMIN_USER
_html = ''
if qs.exists():
    error = qs.first()
    data = error.data.get('errors', [])
    for i in data:
        _html += '<hr>'
        _html += '<h2>Ошибки скрапинга</h2>'
        _html += f'<p><a href="{i["url"]}">Error: {i["title"]}</a></p>'
    subject = f'Ошибки скрапинга {today}'
    text_content = 'Ошибки скрапинга'
    data = error.data.get('user_data', [])
    if data:
        _html += '<hr>'
        _html += '<h2>Пожелания пользователей</h2>'
        for i in data:
            _html += f'<p>>Город: {i["city"]}, Язык программирования: {i["language"]}, Email: {i["email"]}</p>'
        subject = f'Пожелания пользователей  {today}'
        text_content = 'Пожелания пользователей'


qs = Url.objects.all().values('city', 'language')
urls_dct = {(i['city'], i['language']): True for i in qs}
urls_errors = ''
for keys in users_dct.keys():
    if keys not in urls_dct:
        _html += '<hr>'
        _html += '<h2>Отсутствующие урлы</h2>'
        if keys[0] and keys[1]:
            urls_errors += f'<p> Для города {keys[0]} и ЯП {keys[1]} отсутствуют Url</p>'
if urls_errors:
    subject += 'Отсутствующие урлы'
    _html += urls_errors

if subject:
    msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
    msg.attach_alternative(_html, "text/html")
    msg.send()
