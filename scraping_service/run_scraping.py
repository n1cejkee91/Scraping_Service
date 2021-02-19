import codecs
import os, sys

from django.contrib.auth import get_user_model
from django.db import DatabaseError

proj = os.path.dirname(os.path.abspath('manage.py'))
sys.path.append(proj)
os.environ["DJANGO_SETTINGS_MODULE"] = "scraping_service.settings"

import django

django.setup()

from scraping.parsers import *
from scraping.models import Vacancy, City, Languages, Errors

User = get_user_model()

parsers = (
    (work, 'https://www.work.ua/jobs-kyiv-python/'),
    (dou, 'https://jobs.dou.ua/vacancies/?category=Python'),
    (rabota, 'https://rabota.ua/zapros/python/%d1%83%d0%ba%d1%80%d0%b0%d0%b8%d0%bd%d0%b0'),
    (djinni, 'https://djinni.co/jobs/keyword-python/kyiv/'),
)


def get_settings_user():
    qs = User.objects.filter(send_email=True).values()
    settings_user_lst = set((q['city_id'], q['language_id']) for q in qs)
    return settings_user_lst


q = get_settings_user()

city = City.objects.filter(slug='kiev').first()
language = Languages.objects.filter(slug='python').first()

jobs, errors = [], []

for func, url in parsers:
    j, e = func(url)
    jobs += j
    errors += e

for job in jobs:
    v = Vacancy(**job, city=city, language=language)
    try:
        v.save()
    except DatabaseError:
        pass
if errors:
    er = Errors(data=errors).save()

#  with codecs.open('work.txt', 'w', 'utf-8') as h:
#      h.write(str(jobs))
