import json
import re
from bs4 import BeautifulSoup
regex = re.compile(r'PT(\d+)H(\d+)M')
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
    movie_data['image'] = raw_data.get('image', default_img)
    movie_data['rate_count'] = raw_data.get(
        'aggregateRating', {'ratingCount': 0})['ratingCount']
    movie_data['rate_value'] = raw_data.get(
        'aggregateRating', {'ratingValue': 0})['ratingValue']
    return movie_data


def return_raw_json(movie_page):
    soup = BeautifulSoup(movie_page, 'lxml')
    raw_data = json.loads(
        soup.find('script', {'type': 'application/ld+json'}).text)
    return raw_data
