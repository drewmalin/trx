from flask import Flask

app = Flask(__name__)
app.database = 'WODTracker.db'
app.debug = True
app.secret_key = 'dev'
# Setup database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///WODTracker.db'

import WODTracker.views
from views import *
from api import *

# HTML page rules
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
app.add_url_rule('/calendar',
	view_func=CalendarView.as_view('calendar'),
	methods=['GET'])

# API rules
app.add_url_rule('/users/',
	defaults={'user_id': None},
	view_func=UserAPI.as_view('user_api'),
	methods=['GET'])
app.add_url_rule('/users/<int:user_id>/', 
	view_func=UserAPI.as_view('user_api'),
	methods=['GET'])
app.add_url_rule('/users/<int:user_id>/workouts/',
	defaults={'workout_id': None},
	view_func=WorkoutAPI.as_view('workout_api'),
	methods=['GET'])
app.add_url_rule('/users/<int:user_id>/workouts/<int:workout_id>/', 
	view_func=WorkoutAPI.as_view('workout_api'),
	methods=['GET'])
app.add_url_rule('/users/<int:user_id>/exercises/',
	defaults={'exercise_name': None},
	view_func=ExerciseAPI.as_view('exercise_api'),
	methods=['GET'])
app.add_url_rule('/users/<int:user_id>/exercises/<string:exercise_name>/',
	view_func=ExerciseAPI.as_view('exercise_api'),
	methods=['GET'])

from utilities import db


# Uncomment when db refreshes are needed
# db.drop_all()
# db.create_all()
