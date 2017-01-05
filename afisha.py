import json
import re
import requests
from bs4 import BeautifulSoup
url = 'http://www.afisha.ru/msk/schedule_cinema/'
regex = re.compile(r'PT(\d+)H(\d+)M')


def get_movie_links(url):
    soup = BeautifulSoup(requests.get(url).text, 'lxml')
    a_elements = soup.findAll(string=re.compile(r'\w+'),
                              href=re.compile(r'movie/[0-9]+'))
    return ['http:' + el['href'] for el in a_elements]


def collect_movie_data(url):
    soup = BeautifulSoup(requests.get(url).text, 'lxml')
    raw_data = json.loads(
        soup.find('script', {'type': 'application/ld+json'}).text)
    movie_data = {}
    duration = raw_data.get('duration', {'name': 'Не известно'})['name']
    movie_data['duration'] = regex.sub(lambda m: str(
        int(m.group(1)) * 60 + int(m.group(2))), duration)
    movie_data['director'] = raw_data.get(
        'director', {'name': 'Неизвестен'})['name']
    movie_data['title'] = raw_data['name']
    movie_data['year'] = re.sub(
        r'(\d{4}).*', r'\1', raw_data['datePublished'])
    movie_data['description'] = raw_data['description']
    movie_data['url'] = raw_data['url']
    movie_data['genre'] = raw_data['genre']
    movie_data['text'] = raw_data.get('text', 'Нет описания')
    movie_data['image'] = raw_data.get('image', 'Нет изображения')
    movie_data['rate_count'] = raw_data.get(
        'aggregateRating', {'ratingCount': 0})['ratingCount']
    movie_data['rate_value'] = raw_data.get(
        'aggregateRating', {'ratingValue': 0})['ratingValue']
    return movie_data
