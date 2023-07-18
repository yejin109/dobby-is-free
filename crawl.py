import requests
from requests_html import HTMLSession
from selenium import webdriver
from bs4 import BeautifulSoup
import time


def get_arxiv(url, target_date):
    response = requests.get(url)

    if response.status_code == 200:
        html = response.text
        soup = BeautifulSoup(html, 'html.parser')
        dlpage = soup.find('div', id='dlpage')

        dates = [i.text for i in dlpage.find_all('h3')]
        assert target_date in dates, f"Out of dates"

        dls = dlpage.find_all('dl')
        date_id = dates.index(list(filter(lambda d: d == target_date, dates))[0])

        dl = dls[date_id]
        # dl = dlpage.find('dl')
        dts = dl.find_all('dt')
        dds = dl.find_all('dd')

        papers = list()
        for dt, dd in zip(dts, dds):
            _link = 'https://arxiv.org'+dt.span.find_all('a')[0]['href']
            _title = dd.find('div', 'meta').find('div', 'list-title mathjax').text.strip('\n')[7:]

            papers.append({'title': _title, 'link': _link})
        return papers

    else:
        assert False, f"Error in crawl {response.status_code}"


def get_icml(url_base, year, keyword: str):
    keyword = keyword.replace(' ', '+')
    url = url_base.format(year=year) + f"&search={keyword}"
    driver = webdriver.Chrome()
    driver.get(url)
    time.sleep(10)
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    cards = soup.find('div', 'cards row')
    # cards = list(filter(lambda d: cards_filter(d), divs))

    papers = list()
    for card in cards:
        tag_a = card.find('a')
        _link = f'https://icml.cc/virtual/{year}/' + tag_a['href']
        _title = tag_a.text.strip('\n ')
        papers.append({'title': _title, 'link': _link})
    driver.close()
    assert len(papers) != 0, f"No papers for {keyword} in {year}"
    return papers
