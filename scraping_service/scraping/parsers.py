'''Парсер для сайта work.ua'''

import requests
import codecs
from bs4 import BeautifulSoup as BS
from random import randint

__all__ = ('work', 'rabota', 'dou', 'djinni')

headers = [
    {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'},
    {'User-Agent': 'Mozilla/5.0 (X11; OpenBSD i386) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.125 Safari/537.36'},
    {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:77.0) Gecko/20190101 Firefox/77.0'},
    {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Edge/18.19582'}
]


def work(url):
    jobs = []
    errors = []
    url = 'https://www.work.ua/jobs-kyiv-python/'
    domain = 'https://www.work.ua'
    resp = requests.get(url, headers=headers[randint(0, 3)])
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
    resp = requests.get(url, headers=headers[randint(0, 3)])
    if resp.status_code == 200:
        soup = BS(resp.content, 'html.parser')
        not_new_jobs = soup.find('div', attrs={'class': 'f-vacancylist-newnotfound'})  # Новых вакансий не найдено
        if not not_new_jobs:  # Если новые вакансии есть!
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
                        jobs.append(
                            {'title': title.text, 'url': domain + href, 'description': content, 'company': company})
            else:
                errors.append({'url': url, 'title': "Table doesn't exist"})
        else:
            errors.append({'url': url, 'title': 'Page is empty'})
    else:
        errors.append({'url': url, 'title': 'Page not found'})
    return jobs, errors


def dou(url):
    jobs = []
    errors = []
    resp = requests.get(url, headers=headers[randint(0, 3)])
    if resp.status_code == 200:
        soup = BS(resp.content, 'html.parser')
        main_div = soup.find('div', id='vacancyListId')
        if main_div:
            li_lst = main_div.find_all('li', attrs={'class': 'l-vacancy'})
            for li in li_lst:
                title = li.find('div', attrs={'class': 'title'})
                href = title.a['href']
                div_content = li.find('div', attrs={'class': 'sh-info'})
                content = div_content.text
                company = 'No name'
                a_company = title.find('a', attrs={'class': 'company'})
                if a_company:
                    company = a_company.text
                jobs.append({'title': title.text, 'url': href, 'description': content, 'company': company})
        else:
            errors.append({'url': url, 'title': "Div doesn't exist"})
    else:
        errors.append({'url': url, 'title': 'Page not found'})
    return jobs, errors


def djinni(url):
    jobs = []
    errors = []
    domain = 'https://djinni.co'
    resp = requests.get(url, headers=headers[randint(0, 3)])
    if resp.status_code == 200:
        soup = BS(resp.content, 'html.parser')
        main_ul = soup.find('ul', attrs={'class': 'list-unstyled list-jobs'})
        if main_ul:
            li_lst = main_ul.find_all('li', attrs={'class': 'list-jobs__item'})
            for li in li_lst:
                title = li.find('div', attrs={'class': 'list-jobs__title'})
                href = title.a['href']
                div_content = li.find('div', attrs={'class': 'list-jobs__description'})
                content = div_content.text
                company = 'No name'
                div_company = li.find('div', attrs={'class': 'list-jobs__details__info'})
                if div_company:
                    company = div_company.text
                jobs.append({'title': title.text, 'url': domain + href, 'description': content, 'company': company})
        else:
            errors.append({'url': url, 'title': "Div doesn't exist"})
    else:
        errors.append({'url': url, 'title': 'Page not found'})
    return jobs, errors


if __name__ == '__main__':
    url = 'https://djinni.co/jobs/keyword-python/kyiv/'
    jobs, errors = djinni(url)
    with codecs.open('work.txt', 'w', 'utf-8') as h:
        h.write(str(jobs))
