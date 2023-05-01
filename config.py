import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    # Web form
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'

    # Database: defaulting to SQLite
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(os.path.dirname(__file__), 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Pagination: int() used to convert string value to integer
    POSTS_PER_PAGE = int(os.environ.get('POSTS_PER_PAGE')) or 5

    # Search
    ELASTICSEARCH_URL = os.environ.get('ELASTICSEARCH_URL')
    