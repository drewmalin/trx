# API!
#
# Many of the JSON strings constructed below are done so in an odd manner (e.g. having a single line do something
# like 'json+="{"') -- this is purely for readability.
#
# Current API:
# 
# All Users:
# 	/users/
# User with id = user_id:						
# 	/users/<user_id>
# All workouts for user with id = user_id:					
# 	/users/<user_id>/workouts/
# Workout with id workout_id for user with id = user_id:
# 	/users/<user_id>/workouts/<workout_id>
# All workotus with exercise = exercise_name for user with id = user_id:
# 	/users/<user_id>/exercises/<exercise_name/

from utilities import db
import flask, flask.views
from models import *
from WODTracker import app
from datetime import datetime, date
from decorators import *
from flask.ext.login import *

class UserAPI(flask.views.MethodView):
	@crossdomain(origin='*')
	def get(self, user_id):
		jsonStr = ""
		users = None
		if user_id is None:
			# Retrieve all users
			users = User.query.order_by(User.username.asc())
			if users is None:
				jsonStr = ""
			else:
				jsonStr = "["
				for user in users:
					jsonStr += "{"
					jsonStr += "\"name\":" + "\""+ user.username + "\""
					jsonStr += "},"
				jsonStr = jsonStr[:-1] + "]"
		else:
			# Retrieve specific user
			user = User.query.filter_by(id=int(user_id)).first()
			if user is None:
				jsonStr = ""
			else:
				jsonStr = "[{\"name\":\"" + user.username + "\"}]"
		return jsonStr
		

class WorkoutAPI(flask.views.MethodView):
	@crossdomain(origin='*')
	def get(self, user_id, workout_id):
		jsonStr = ""
		workouts = None
		if user_id is None:
			# No user id? Return empty string
			pass
		else:
			if workout_id is None:
				# Retrieve all workouts for user
				workouts = Workout.query.filter_by(user_id=user_id).order_by(Workout.date.asc())
				if workouts is None:
					jsonStr = ""
				else:
					jsonStr = "["
					for workout in workouts:
						jsonStr += "{"
						jsonStr += "\"workout_id\":" + "\"" + str(workout.id) + "\","
						jsonStr += "\"exercise_name\":" + "\"" + workout.exercise.name + "\","
						jsonStr += "\"units\":" + "\"" + str(workout.units) + "\","
						jsonStr += "\"uom\":" + "\"" + workout.exercise.uom + "\","
						jsonStr += "\"extra_credit\":" + "\"" + workout.extra_credit + "\","
						jsonStr += "\"date\":" + "\"" + workout.date.strftime('%m/%d/%Y') + "\""
						jsonStr += "},"
					jsonStr = jsonStr[:-1] + "]"
			else:
				# Retrieve specific workout
				workout = Workout.query.filter_by(user_id=int(user_id), id=int(workout_id)).first()
				if workout is None:
					jsonStr = ""
				else:
					jsonStr = "[{\"workout_id\":\""+str(workout.id)+"\",\"exercise_name\":\""+workout.exercise.name+"\",\"units\":\""+str(workout.units)+"\","
					jsonStr += "\"uom\":\""+workout.exercise.uom+"\",\"extra_credit\":\""+workout.extra_credit+"\","
					jsonStr += "\"date\":\""+workout.date.strftime('%m/%d/%Y')+"\"}]"
		return jsonStr


class ExerciseAPI(flask.views.MethodView):
	@crossdomain(origin='*')
	def get(self, user_id, exercise_name):
		jsonStr = ""
		exercise = None
		workouts = None
		if user_id is None:
			# No user id? Return empty string
			jsonStr = ""
		else:
			# Retrieve all workouts for all exercises
			if exercise_name is None:
				workouts = Workout.query.filter_by(user_id=user_id).order_by(Workout.date.asc())
			# Retrieve all workouts for specific exercise
			else:
				exercise = Exercise.query.filter_by(name=exercise_name).first()
				if exercise is None:
					jsonStr = ""
				else:
					workouts = Workout.query.filter_by(user_id=user_id, exercise_id=int(exercise.id)).order_by(Workout.date.asc())
			if workouts is None:
				jsonStr = ""
			else:
				jsonStr = "["
				for workout in workouts:
					jsonStr += "{"
					jsonStr += "\"exercise_name\":" + "\"" + workout.exercise.name + "\","
					jsonStr += "\"units\":" + "\"" + str(workout.units) + "\","
					jsonStr += "\"uom\":" + "\"" + workout.exercise.uom + "\","
					jsonStr += "\"extra_credit\":" + "\"" + workout.extra_credit + "\","
					jsonStr += "\"date\":" + "\"" + workout.date.strftime('%m/%d/%Y') + "\""
					jsonStr += "},"
				jsonStr = jsonStr[:-1] + "]"
		return jsonStr

# The calendar widget is silly and requires a feed-like pattern where instead of simply *accepting* JSON to build
# its data, it needs a URL which in turn will provide the JSON. That means that the normal API won't necessarily
# work, as the widget wants the feed to provide data in the format that it specifies. Thus, we have a special
# interface for the calendar:
@app.route('/calendar_feed')
@crossdomain(origin='*')
def request_calendar():
	jsonStr = "["
	workouts = Workout.query.filter_by(user_id=current_user.id)

	for workout in workouts:
		jsonStr += "{"
		jsonStr += "\"id\":" + str(workout.id) + ","
		jsonStr += "\"title\":" + "\"" + workout.exercise.name + "\","
		jsonStr += "\"start\":" + "\"" + workout.date.strftime('%Y-%m-%d') + "\","
		jsonStr += "\"allDay\":true}"
		jsonStr += ","

	jsonStr = jsonStr[:-1] + "]"
	
	return jsonStr