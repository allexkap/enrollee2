from parse import Handler
from bs4 import BeautifulSoup
import requests


def forceint(cell):
    part = cell.strip(' 0').strip('.') # .replace(',', '.')
    if not part: part = '0'
    assert part.isdecimal()
    return int(part)

def get(url):
    response = requests.get(url)
    assert response.status_code == 200
    raw = response.text.encode(response.encoding).decode()
    return BeautifulSoup(raw, "html.parser")

def pretty(data, metadata):
    out = f'{metadata["time"]}\n'\
    f'{metadata["title"]}\n'\
    f'Бюджетных мест: {metadata["total"]}\n'\
    f'Из них БВИ: {data["bvi"]}\n'\
    f'Согласий: {data["sgl"]}\n\n'\
    f'Свободных: {metadata["total"]-data["bvi"]-data["sgl"]}\n'\
    f'Заявлений: {data["ege"]}'
    return out


def spbgu(page):
    score = {key: 0 for key in ('lrcfpd', )[page]}
    url = 'https://cabinet.spbu.ru/Lists/1k_EntryLists/list_{}.html'.format(
        (
            '',
        )[page]
    )

    soup = get(url)

    metadata = {}
    p = soup.select('p')
    metadata['time'] = p[1].text.split()[-1]
    p = p[0].text.split('\n')
    metadata['title'] = p[4].split(':')[1].strip()
    metadata['total'] = forceint(p[8].split()[-1])
    yield metadata, None

    data = {}
    for line in soup.find_all('tr')[1:]:
        cells = [cell.text for cell in line.find_all('td')]
        data['bvi'] = (cells[2] == 'Без ВИ')
        data['sgl'] = (cells[10] == 'Да')
        if data['bvi']:
            assert data['sgl']
            yield data, None
        else:
            for i, key in enumerate(score):
                score[key] = forceint(cells[i+6])
            yield data, score
