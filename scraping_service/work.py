'''Парсер для сайта work.ua'''

import requests
import codecs
from bs4 import BeautifulSoup as BS

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'}

url = 'https://www.work.ua/jobs-kyiv-python/'

domain = 'https://www.work.ua'

resp = requests.get(url, headers=headers)

jobs = []
errors = []

if resp.status_code == 200:
    soup = BS(resp.content, 'html.parser')
    main_div = soup.find('div', id='pjax-job-list')
    if main_div:
        div_lst = main_div.find_all('div', attrs={'class': 'job-link'})
        for div in div_lst:
            title = div.find('h2')
            href = title.a['href']
            content = div.p.text
            company = 'No name'
            logo = div.find('img')
            if logo:
                company = logo['alt']
            jobs.append({'title': title.text, 'url': domain + href, 'description': content, 'company': company})
    else:
        errors.append({'url': url, 'title': "Div doesn't exist"})
else:
    errors.append({'url': url, 'title': 'Page not found'})

with codecs.open('work.txt', 'w', 'utf-8') as h:
    h.write(str(jobs))
