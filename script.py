from parse import Handler
from bs4 import BeautifulSoup
import requests
import re


def intfloat(string, mode=0):
    try:
        return int(float(string))
    except Exception as e:
        return mode

def get(url):
    response = requests.get(url)
    assert response.status_code == 200
    raw = response.text.encode(response.encoding).decode()
    return BeautifulSoup(raw, "html.parser")

def pretty(data):
    out = f'{data["title"]}\n'\
    f'Бюджетных мест: {data["total"]}\n'\
    f'Из них БВИ: {data["bvi"]}\n'\
    f'Согласий: {data["sgl"]}\n'\
    f'Свободных: {data["total"]-data["bvi"]-data["sgl"]}\n'\
    f'Заявлений: {data["ege"]}\n'\
    f'От {data["time"]}'
    return out


def _spbu(uid, url):
    soup = get(url)

    data = {}
    part = soup.select('p')
    data['time'] = part[1].text.split()[-1]
    part = part[0].text.split('\n')
    data['title'] = re.search(r'\d (.+)', part[4])[1]
    data['total'] = int(part[8].split()[-1])

    for line in soup.select('tr')[1:]:
        if line.select('td')[1].text == uid:
            cells = [cell.text for cell in line.select('td')]
            scores = []
            while (score:=intfloat(cells[6+len(scores)], mode='')) != '':
                scores.append(score)
            break
    yield data, scores

    data = {}
    count = len(scores)
    for line in soup.select('tr')[1:]:
        cells = [cell.text for cell in line.select('td')]
        if cells[1] == uid:
            continue
        data['bvi'] = cells[2] == 'Без ВИ'
        data['sgl'] = cells[10] == 'Да'
        if not data['bvi']:
            scores = map(intfloat, cells[6:6+count])
        else:
            assert data['sgl']
            scores = None
        yield data, scores


url = 'https://cabinet.spbu.ru/Lists/1k_EntryLists/list_.html'
spbu = Handler(_spbu, '___-___-___ __')
out = pretty(spbu(url))
print(out)
