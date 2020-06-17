import os

basedir = os.path.abspath(os.path.dirname(__file__))
name_db = 'my_db.sqlite3'


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI = f'sqlite:///{os.path.join(basedir, name_db)}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    TMDB_API_KEY = '312687a97cbd4f1bb0cb2571ca051c0f'
    TIME_OUT_S = 5
