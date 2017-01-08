from flask import Flask, render_template, Response, json
from werkzeug.contrib.cache import SimpleCache
import requests
from afisha import collect_movie_data, return_raw_json, get_movies_urls

app = Flask(__name__)
cache = SimpleCache()
app.config['JSON_AS_ASCII'] = False
afisha_url = 'http://www.afisha.ru/msk/schedule_cinema/'


def get_from_cache(url, timeout=43200):
    page = cache.get(url)
    if page:
        return page
    page = requests.get(url).text
    cache.add(url, page, timeout=timeout)
    return page


@app.route('/')
def films_list():
    main_page = get_from_cache(afisha_url)
    links = get_movies_urls(main_page)
    movie_list = []
    for link in set(links):
        movie_page = get_from_cache(link)
        movie_data = collect_movie_data(movie_page)
        movie_list.append(movie_data)
    return render_template('films_list.html', movies=movie_list)


@app.route('/api')
def api_about():
    return render_template('api_about.html')


@app.route('/api/movies_list', methods=['GET'])
def api_movies_list():
    main_page = get_from_cache(afisha_url)
    links = get_movies_urls(main_page)
    movies_json = []
    for link in links:
        movie_page = get_from_cache(link)
        movies_json.append(return_raw_json(movie_page))
    return Response(json.dumps(movies_json, indent=4),
                    content_type='application/json; charset=utf-8')


@app.route('/api/movie/<int:param>/', methods=['GET'])
def movie_api(param):
    url = 'http://www.afisha.ru/movie/{}'.format(param)
    page = get_from_cache(url)
    json_data = return_raw_json(page)
    return Response(json.dumps(json_data, indent=4),
                    content_type='application/json; charset=utf-8')


if __name__ == "__main__":
    app.run(debug=True)
