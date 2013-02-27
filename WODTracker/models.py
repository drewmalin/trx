from utilities import db

#---------------- Models ----------------#
class User(db.Model): 
	__tablename__ = 'User'
	id 			= db.Column(db.Integer, primary_key=True)
	username 	= db.Column(db.String(80))
	password 	= db.Column(db.String(100))
	workouts	= db.relationship('Workout', backref='user')

	def __init__(self, username, password):
		self.username = username
		self.password = password

class Workout(db.Model):
	__tablename__ = 'Workout'
	id 				= db.Column(db.Integer, primary_key=True)
	user_id 		= db.Column(db.Integer, db.ForeignKey('User.id'))
	exercise_id		= db.Column(db.Integer, db.ForeignKey('Exercise.id'))
	exercise        = db.relationship('Exercise', backref='workouts')
	units 			= db.Column(db.Integer)
	extra_credit 	= db.Column(db.String(100))
	date            = db.Column(db.Date)

	def __init__(self, uid, exercise_id, units, ec, date):
		self.user_id 		= uid
		self.exercise_id	= exercise_id
		self.units 			= units
		self.extra_credit 	= ec
		self.date		= date

class Exercise(db.Model):
	__tablename__ = 'Exercise'
	id 			  = db.Column(db.Integer, primary_key=True)
	name 		  = db.Column(db.String(100))
	uom			  = db.Column(db.String(100))
	description   = db.Column(db.String(100))

	def __init__(self, name, uom, description):
		self.name 			= name
		self.uom		    = uom
		self.description 	= description
