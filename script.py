from parse import Handler
from bs4 import BeautifulSoup
import requests
import re


def intfloat(string, mode=0):
    try:
        return int(float(string.replace(',', '.')))
    except Exception as e:
        return mode

def get(url):
    response = requests.get(url, verify=False)
    assert response.status_code == 200
    raw = response.text.encode(response.encoding).decode()
    return BeautifulSoup(raw, "html.parser")



def _spbu(uid, url):
    soup = get(url)

    data = {}
    part = soup.select('p')
    assert len(part) < 4    # Квоты не учитываются
    data['time'] = part[0].text.split()[-1]
    data['title'] = re.search(r'\d ([\w ]+)', part[1].text)[1]
    data['total'] = int(re.search(r'\d+', part[2].text)[0])

    for line in soup.select('tr')[1:]:
        if uid in line.select('td')[1].text:
            cells = [cell.text for cell in line.select('td')]
            scores = []
            while (score:=intfloat(cells[len(scores)+3], mode='')) != '':
                scores.append(score)
            break
    else:
        raise ValueError
    yield data, scores

    data = {}
    count = len(scores)
    for line in soup.select('tr')[1:]:
        cells = [cell.text for cell in line.select('td')]
        if uid in cells[1]:
            continue
        data['bvi'] = 'Без ВИ' in [count+4]
        data['sgl'] = 'Да' in cells[count+5]
        if not data['bvi']:
            scores = [*map(intfloat, cells[3:3+count])]
        else:
            scores = None
        yield data, scores


def _spbstu(uid, url):
    soup = get(url)

    data = {}
    data['title'] = re.search(r'\d ([\w ]+)', soup.h2.text)[1]
    data['total'] = 0 # todo
    data['time'] = soup.footer.text.split()[-1][:-3]
    yield data, (0, 0, 0, 0) # todo

    data = {}
    for line in soup.select('tr')[1:]:
        cells = [cell.text for cell in line.select('td')]
        if uid in cells[1]:
            continue
        data['bvi'] = '✓' in cells[0] # todo
        data['sgl'] = '✓' in cells[0] # todo
        if not data['bvi']:
            scores = [*map(intfloat, cells[4:8])]
        else:
            scores = None
        yield data, scores


def _itmo(uid, url):
    with open(url, errors='ignore') as file:
        soup = BeautifulSoup(file.read(), "html.parser")

    data = {}
    table, = soup.select('.RatingPage_rating__1ACLE')
    it = table.children
    data['title'] = re.search(r'\d ([\w ]+)', next(it).text)[1]
    text = next(it).text
    data['total'] = int(re.search(r': (\d+)', text)[1])
    data['time'] = re.search(r' (\d{2}:\d{2}):\d{2}', text)[1]
    yield data, (0, 0, 0, 0) # todo

    data = {}
    try:
        while True:
            data['bvi'] = next(it).text != 'Общий конкурс' # todo
            for line in next(it).children:
                cells = line.select('span')
                if uid in line.select('p')[1].text:
                    continue
                if data['bvi']:
                    scores = None
                    data['sgl'] = cells[2].text[-2:] == 'да'
                else:
                    scores = [intfloat(cells[i].text) for i in (0, 0, 0, 0)] # todo
                    data['sgl'] = cells[6].text[-2:] == 'да'
                yield data, scores

    except StopIteration:
        pass
