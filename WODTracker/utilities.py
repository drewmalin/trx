from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager
from WODTracker import app

db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.setup_app(app)

