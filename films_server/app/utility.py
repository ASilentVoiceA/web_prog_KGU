import tmdbsimple as tmdb
from config import Config

tmdb.API_KEY = Config.TMDB_API_KEY


def img_to_movie(movie_list):
    for item in movie_list:
        if item['poster_path'] is not None:
            item['image'] = f'https://image.tmdb.org/t/p/w600_and_h900_bestv2{item["poster_path"]}'
        else:
            item['image'] = 'static/img/poster_none.png'

    return movie_list


def search_movie(movie_name):
    movie_list = []
    error = ''
    try:
        movie_list = list(tmdb.Search().movie(language='ru', query=movie_name)['results'])

        if len(movie_list) > 0:
            movie_list = img_to_movie(movie_list)
        else:
            error = 'Фильм не найден'
    except:
        error = 'Ошибка соединение с сервером'

    return movie_list, error
