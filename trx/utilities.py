from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager
from trx import app

db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)