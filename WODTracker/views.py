from utilities import db
import flask, flask.views
from models import *
from WODTracker import app
from flask.ext.login import *
from datetime import datetime, date

# All workouts for a user
@app.route('/_request_workouts')
def request_workouts():
	exerciseReq = flask.request.args.get('exercise', '', type=str)
	exercise = Exercise.query.filter_by(name=exerciseReq).first()
	workouts = Workout.query.filter_by(user_id=current_user.id, exercise_id=int(exercise.id))
	workoutListStr = ""
	workoutDateStr = ""

	for workout in workouts:
		workoutListStr += "\"" + str(workout.units) + "\","
		workoutDateStr += "\"" + workout.date.strftime('%m/%d/%Y') + "\","

	workoutListStr = workoutListStr[:-1]
	workoutDateStr = workoutDateStr[:-1]

	return '{"name":\"'+exercise.name+'\","units":\"'+exercise.uom+'\","arr":['+workoutListStr+'],"dates":['+workoutDateStr+']}'

# Full calendar for a user
@app.route('/_request_calendar')
def request_calendar():
	workouts = Workout.query.filter_by(user_id=flask.session['uid'])
	fullStr = "["

	for workout in workouts:
		fullStr += "{"
		fullStr += "\"id\":" + str(workout.id) + ","
		fullStr += "\"title\":" + "\"" + workout.exercise.name + "\","
		fullStr += "\"start\":" + "\"" + workout.date.strftime('%Y-%m-%d') + "\","
		fullStr += "\"allDay\":true}"
		fullStr += ","

	fullStr = fullStr[:-1] + "]"

	return fullStr
	
# Single workout for a user
@app.route('/_request_workout')
def request_workout():
	workoutID = flask.request.args.get('workoutID', '', type=int)
	workout = Workout.query.filter_by(user_id=flask.session['uid'], id=workoutID).first()

	return '{"units":"'+str(workout.units)+'","uom":"'+workout.exercise.uom+'"}'

#---------------- Views ----------------#
class Index(flask.views.MethodView):
	def get(self):
		if not current_user.is_anonymous() and User.query.count() > 0:
			user = User.query.filter_by(id=current_user.id).first()
			workouts = user.workouts
			exercises = Exercise.query.order_by(Exercise.name).all()
			return flask.render_template('user.html', workouts=workouts, exercises=exercises)
		else:
                        logout_user()
			return flask.render_template('user.html')
	def post(self):
		# Handle logout request
		if 'logout' in flask.request.form:
                        logout_user()
			return flask.redirect(flask.url_for('index'))
		
		# Ensure username and password are provided
		if flask.request.form['username'] == "":
			flask.flash("Username is required!")
			return flask.redirect(flask.url_for('index'))
		elif flask.request.form['password'] == "":
			flask.flash("Password is required!")
			return flask.redirect(flask.url_for('index'))

		username = flask.request.form['username']
		password = flask.request.form['password']
		user = User.query.filter_by(username=username, password=password).first()
        
		# Query user table
		if not user:
			flask.flash("Username or password is incorrect!")
			return flask.redirect(flask.url_for('index'))
		else:
                        login_user(user)
			return flask.redirect(flask.url_for('index'))

class NewUser(flask.views.MethodView):
	def get(self):
		return flask.render_template('newUser.html')
	def post(self):
		# Ensure username and password are provided, that
		# the username is available, and that the passwords
		# match
		if flask.request.form['username'] == "":
			flask.flash("Username is required!")
			return flask.redirect(flask.url_for('new_user'))
		elif flask.request.form['password1'] == "" or flask.request.form['password2'] == "":
			flask.flash("Both password fields are required!")
			return flask.redirect(flask.url_for('new_user'))
		elif flask.request.form['password1'] != flask.request.form['password2']:
			flask.flash("Passwords must match!")
			return flask.redirect(flask.url_for('new_user'))
		elif User.query.filter_by(username=flask.request.form['username']).first() != None:
			flask.flash("Username already in use!")
			return flask.redirect(flask.url_for('new_user'))

		# Username/password is valid, persist new user
		username = flask.request.form['username']
		password = flask.request.form['password1']
		user = User(username, password)

		db.session.add(user)
		db.session.commit()

                #Log the user in
                login_user(user)
		return flask.redirect(flask.url_for('index'))

class WorkoutView(flask.views.MethodView):
	def get(self):
		exercises = Exercise.query.order_by(Exercise.name).all()
		return flask.render_template('workout.html', exercises=exercises)
	def post(self):
		if flask.request.form['exerciseselect'] == "":
			flask.flash("Exercise is required!")
			return flask.redirect(flask.url_for('workout'))
		elif flask.request.form['result'] == "":
			flask.flash("Result is required!")
			return flask.redirect(flask.url_for('workout'))
		elif flask.request.form['date'] == "":
			flask.flash("Date is required!")
			return flask.redirect(flask.url_for('workout'))

		exercise = Exercise.query.filter_by(name=flask.request.form['exerciseselect']).first().id
		results  = flask.request.form['result']
		ec 		 = flask.request.form['extracredit']
		datestr     = flask.request.form['date']
                date        = datetime.strptime(datestr, '%m/%d/%Y').date()
		workout  = Workout(current_user.id, exercise, results, ec, date)

		db.session.add(workout)
		db.session.commit()

		return flask.redirect(flask.url_for('index'))

class ExerciseView(flask.views.MethodView):
	def get(self):
		return flask.render_template('newExercise.html')
	def post(self):
		if flask.request.form['name'] == "":
			flask.flash("Exercise name is required!")
			return flask.redirect(flask.url_for('new_exercise'))
		elif flask.request.form['uom'] == "":
			flask.flash("Unit of Measure is required!")
			return flask.redirect(flask.url_for('new_exercise'))


		name = flask.request.form['name']
		uom  = flask.request.form['uom']
		desc = flask.request.form['description']
		exercise = Exercise(name, uom, desc)

		db.session.add(exercise)
		db.session.commit()

		return flask.redirect(flask.url_for('workout'))

class WeighInView(flask.views.MethodView):
	def get(self):
		return flask.render_template('weighin.html')
	def post(self):
		return 'hi'

class CalendarView(flask.views.MethodView):
	def get(self):
		return flask.render_template('calendar.html')
