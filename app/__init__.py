import socket
from flask import Flask
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect

from config import Config
from flask_moment_project import Moment

socket.setdefaulttimeout(Config.TIME_OUT_S)

app = Flask(__name__)
app.config.from_object(Config)
csrf = CSRFProtect(app)

db = SQLAlchemy(app)
migrate = Migrate(app, db)
login = LoginManager(app)
moment = Moment(app)

from app import routes, models

