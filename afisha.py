import json
import re
from bs4 import BeautifulSoup
default_img = 'http://www.userlogos.org/files/logos/klonex/af.jpg'


def get_movies_urls(main_page):
    soup = BeautifulSoup(main_page, 'lxml')
    a_elements = soup.findAll(string=re.compile(r'\w+'),
                              href=re.compile(r'movie/[0-9]+'))
    return ['http:' + el['href'] for el in a_elements]


def collect_movie_data(movie_page):
    soup = BeautifulSoup(movie_page, 'lxml')
    raw_data = json.loads(
        soup.find('script', {'type': 'application/ld+json'}).text)
    duration = raw_data.get('duration', {'name': 'Не известно'})['name']
    duration = re.sub(r'PT(\d+)H(\d+)M', lambda m: str(
        int(m.group(1)) * 60 + int(m.group(2))), duration)
    director = raw_data.get('director', {'name': 'Неизвестен'})['name']
    year = re.sub(r'(\d{4}).*', r'\1', raw_data['datePublished'])
    rate_count = raw_data.get(
        'aggregateRating', {'ratingCount': 0})['ratingCount']
    rate_value = raw_data.get(
        'aggregateRating', {'ratingValue': 0})['ratingValue']
    movie_data = {
            'text': raw_data.get('text', 'Нет описания'),
            'image': raw_data.get('image', default_img),
            'description': raw_data['description'],
            'genre': raw_data['genre'],
            'title': raw_data['name'],
            'url': raw_data['url'],
            'rate_count': rate_count,
            'rate_value': rate_value,
            'duration': duration,
            'director': director,
            'year': year,
            }
    return movie_data


def return_raw_json(movie_page):
    soup = BeautifulSoup(movie_page, 'lxml')
    raw_data = json.loads(
        soup.find('script', {'type': 'application/ld+json'}).text)
    return raw_data
