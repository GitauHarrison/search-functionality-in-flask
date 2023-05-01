from flask import Flask
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_moment import Moment
from config import Config
from elasticsearch import Elasticsearch


app = Flask(__name__)
app.config.from_object(Config)

# Access value from the config module
app.elasticsearch = Elasticsearch([app.config['ELASTICSEARCH_URL']]) \
    if app.config['ELASTICSEARCH_URL'] else None

boostrap = Bootstrap(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db, render_as_batch=True)
moment = Moment(app)

from app import routes, errors, errors
