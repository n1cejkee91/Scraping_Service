'''Парсер для сайта work.ua'''

import requests
import codecs
from bs4 import BeautifulSoup as BS

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'}


def work(url):
    jobs = []
    errors = []
    url = 'https://www.work.ua/jobs-kyiv-python/'
    domain = 'https://www.work.ua'
    resp = requests.get(url, headers=headers)
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
    return jobs, errors


def rabota(url):
    jobs = []
    errors = []
    domain = 'https://rabota.ua/'
    resp = requests.get(url, headers=headers)
    if resp.status_code == 200:
        soup = BS(resp.content, 'html.parser')
        table = soup.find('table', id='ctl00_content_vacancyList_gridList')
        if table:
            tr_lst = table.find_all('tr', attrs={'id': True})
            for tr in tr_lst:
                div = tr.find('div', attrs={'class': 'card-body'})
                if div:
                    title = div.find('h2', attrs={'class': 'card-title'})
                    href = title.a['href']
                    content_div = div.find('div', attrs={'class': 'card-description'})
                    if content_div:
                        content = content_div.text
                    company = 'No name'
                    company_p = div.find('p', attrs={'class': 'company-name'})
                    if company_p:
                        company = company_p.a.text
                    jobs.append({'title': title.text, 'url': domain + href, 'description': content, 'company': company})
        else:
            errors.append({'url': url, 'title': "Div doesn't exist"})
    else:
        errors.append({'url': url, 'title': 'Page not found'})
    return jobs, errors


if __name__ == '__main__':
    url = 'https://rabota.ua/zapros/python/%d1%83%d0%ba%d1%80%d0%b0%d0%b8%d0%bd%d0%b0'
    jobs, errors = rabota(url)
    with codecs.open('work.json', 'w', 'utf-8') as h:
        h.write(str(jobs))
