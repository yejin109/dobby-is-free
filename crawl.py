import requests
from bs4 import BeautifulSoup


def get_papers(url, target_date):
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
        assert False, f"Error in cralw {response.status_code}"