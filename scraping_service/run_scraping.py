import asyncio
import os
import sys
import datetime as dt

from django.contrib.auth import get_user_model
from django.db import DatabaseError

proj = os.path.dirname(os.path.abspath('manage.py'))
sys.path.append(proj)
os.environ["DJANGO_SETTINGS_MODULE"] = "scraping_service.settings"

import django

django.setup()

from scraping.parsers import *
from scraping.models import Vacancy, Errors, Url

User = get_user_model()

parsers = (
    (work, 'work'),
    (dou, 'dou'),
    (rabota, 'rabota'),
    (djinni, 'djinni'),
    #(msk_rabotaru, 'msk_rabotaru'),
    #(spb_rabotaru, 'spb_rabotaru'),
)

jobs, errors = [], []


def get_settings_url():
    qs = Url.objects.all().values()
    settings_url_lst = set((q['city_id'], q['language_id']) for q in qs)
    return settings_url_lst


def get_urls(settings_for_url):
    qs = Url.objects.all().values()
    url_dct = {(q['city_id'], q['language_id']): q['url_data'] for q in qs}
    urls = []
    for pair in settings_for_url:
        if pair in url_dct:
            tmp = {'city': pair[0], 'language': pair[1]}
            url_data = url_dct.get(pair)
            if url_data:
                tmp['url_data'] = url_dct.get(pair)
                urls.append(tmp)
    return urls


async def main(value):
    func, url, city, language = value
    job, err = await loop.run_in_executor(None, func, url, city, language)
    errors.extend(err)
    jobs.extend(job)


settings_for_url = get_settings_url()
url_list = get_urls(settings_for_url)

loop = asyncio.get_event_loop()
tmp_tasks = [(func, data['url_data'][key], data['city'], data['language'])
             for data in url_list
             for func, key in parsers]

if tmp_tasks:
    tasks = asyncio.wait([loop.create_task(main(f)) for f in tmp_tasks])
    loop.run_until_complete(tasks)
    loop.close()

for job in jobs:
    v = Vacancy(**job)
    try:
        v.save()
    except DatabaseError:
        pass
if errors:
    qs = Errors.objects.filter(timestamp=dt.date.today())
    if qs.exists():
        err = qs.first()
        err.data.update({'errors': errors})
        err.save()
    else:
        er = Errors(data=f'error: {errors}').save()

ten_days_ago = dt.date.today() - dt.timedelta(10)
Vacancy.objects.filter(timestamp__lte=ten_days_ago).delete()
