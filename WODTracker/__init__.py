from flask import Flask

app = Flask(__name__)
app.database = '/tmp/wod.db'
app.debug = True
app.secret_key = 'dev'
# Setup database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///WODTracker.db'

import WODTracker.views
from views import *

app.add_url_rule('/',
	view_func=Index.as_view('index'),
	methods=['GET','POST'])
app.add_url_rule('/newuser',
	view_func=NewUser.as_view('new_user'),
	methods=['GET','POST'])
app.add_url_rule('/recordworkout',
	view_func=WorkoutView.as_view('workout'),
	methods=['GET','POST'])
app.add_url_rule('/newexercise',
	view_func=ExerciseView.as_view('new_exercise'),
	methods=['GET','POST'])
app.add_url_rule('/weighin',
	view_func=WeighInView.as_view('weighin'),
	methods=['GET','POST'])
