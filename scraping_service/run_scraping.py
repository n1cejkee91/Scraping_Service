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
from scraping.models import Vacancy, City, Languages, Errors, Url

User = get_user_model()

parsers = (
    (work, 'work'),
    (dou, 'dou'),
    (rabota, 'rabota'),
    (djinni, 'djinni'),
)


def get_settings_user():
    qs = User.objects.filter(send_email=True).values()
    settings_user_lst = set((q['city_id'], q['language_id']) for q in qs)
    return settings_user_lst


def get_urls(settings_for_user):
    qs = Url.objects.all().values()
    url_dct = {(q['city_id'], q['language_id']): q['url_data'] for q in qs}
    urls = []
    for pair in settings_for_user:
        tmp = {'city': pair[0], 'language': pair[1], 'url_data': url_dct[pair]}
        urls.append(tmp)
    return urls


settings_for_user = get_settings_user()
url_list = get_urls(settings_for_user)

# city = City.objects.filter(slug='kiev').first()
# language = Languages.objects.filter(slug='python').first()

jobs, errors = [], []
for data in url_list:
    for func, key in parsers:
        url = data['url_data'][key]
        j, e = func(url, city=data['city'], language=data['language'])
        jobs += j
        errors += e


for job in jobs:
    v = Vacancy(**job)
    try:
        v.save()
    except DatabaseError:
        pass
if errors:
    er = Errors(data=errors).save()

#  with codecs.open('work.txt', 'w', 'utf-8') as h:
#      h.write(str(jobs))
