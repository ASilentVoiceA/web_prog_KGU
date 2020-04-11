from flask import Flask, render_template, request
import socket
import io
import tmdbsimple as tmdb
from PIL import Image
from urllib.request import urlopen
from multiprocessing import Pool
import base64

tmdb.API_KEY = '312687a97cbd4f1bb0cb2571ca051c0f'
socket.setdefaulttimeout(2)

app = Flask(__name__)


def image_to_byte_array(image: Image):
    imgByteArr = io.BytesIO()
    image.save(imgByteArr, format=image.format)
    imgByteArr = imgByteArr.getvalue()
    return imgByteArr


def download_image(item):
    file_contents = None

    if item['poster_path'] is not None:
        try:
            url_poster_path = 'https://image.tmdb.org/t/p/w600_and_h900_bestv2{}'.format(item['poster_path'])
            image_url = Image.open(urlopen(url_poster_path))
            file_contents = image_to_byte_array(image_url)
        except:
            pass

    if file_contents == None:
        image = Image.open('static/img/poster_none.png')
        file_contents = image_to_byte_array(image)

    base64EncodedStr = base64.b64encode(file_contents).decode('ascii')
    image_output = 'data:image/jpg;base64,{}'.format(base64EncodedStr)

    item['image'] = image_output

    return item


def loade_imge(movie_list):
    count_thread = len(movie_list) // 2

    if count_thread <= 0:
        count_thread = 1

    pool = Pool(count_thread)

    for index, item in enumerate(movie_list):
        item['id_position'] = index

    movie_list = pool.map(download_image, movie_list)
    movie_list = sorted(movie_list, key=lambda k: k['id_position'])

    return movie_list


@app.route("/", methods=['GET', 'POST'])
def main():
    if request.method == 'POST':
        if 'movie_name' in request.form:
            movie_name = request.form['movie_name']

            if len(movie_name) > 0:
                movie_list = list(tmdb.Search().movie(language='ru', query=movie_name)['results'])

                if len(movie_list) > 0:
                    if len(movie_list) > 20:
                        movie_list = movie_list[:20]

                    movie_list = loade_imge(movie_list)

                    return render_template('index_search.html', movie_list=movie_list)

    return render_template('index.html')


if __name__ == '__main__':
    app.run()
