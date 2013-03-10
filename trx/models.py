from flask.ext.login import AnonymousUser
from utilities import db, login_manager
from werkzeug.security import generate_password_hash, check_password_hash

#---------------- Models ----------------#
class User(db.Model): 
    __tablename__ = 'User'
    id                 = db.Column(db.Integer, primary_key=True)
    username         = db.Column(db.String(80))
    password         = db.Column(db.String(100))
    workouts        = db.relationship('Workout', backref='user')
    authenticated    = db.Column(db.Boolean)
    active            = db.Column(db.Boolean)
    admin            = db.Column(db.Boolean)

    def __init__(self, username, password, authenticated=True, active=True, admin=False):
        self.username = username
        self.set_password(password)
        self.authenticated = authenticated
        self.active = active
        self.admin = admin

    def __repr__(self):
        return '<User: %r>' % (self.username)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def is_authenticated(self):
        return self.authenticated

    def is_active(self):
        return self.active

    def is_anonymous(self):
        return False

    def is_admin(self):
        return self.admin

    def get_id(self):
        return unicode(int(self.id))

@login_manager.user_loader
def load_user(userid):
    return User.query.filter_by(id=userid).first()

#Override default login anon user to provide implementation
#of methods that might be called on an anonymous user
class Anonymous(AnonymousUser):
    def is_admin(self):
        return False

class Workout(db.Model):
    __tablename__ = 'Workout'
    id              = db.Column(db.Integer, primary_key=True)
    user_id         = db.Column(db.Integer, db.ForeignKey('User.id'))
    exercise_id     = db.Column(db.Integer, db.ForeignKey('Exercise.id'))
    exercise        = db.relationship('Exercise', backref='workouts')
    units           = db.Column(db.Integer)
    extra_credit    = db.Column(db.String(100))
    date            = db.Column(db.Date)
    is_pr           = db.Column(db.Boolean)

    def __init__(self, uid, eid, units, ec, date):
        self.user_id        = uid
        self.exercise_id    = eid
        self.units          = units
        self.extra_credit   = ec
        self.date           = date
        self.is_pr             = units > Workout.get_current_pr(uid, eid).units

    #Static method that returns the instance of Workout that is the current PR for
    # the user and exercise provided
    @staticmethod
    def get_current_pr(uid, eid):
        curr_pr = Workout.query.filter_by(user_id=uid, exercise_id=eid).\
            order_by(Workout.units.desc()).first()
        return curr_pr

class Exercise(db.Model):
    __tablename__ = 'Exercise'
    id               = db.Column(db.Integer, primary_key=True)
    name           = db.Column(db.String(100))
    uom              = db.Column(db.String(100))
    description   = db.Column(db.String(100))

    def __init__(self, name, uom, description):
        self.name             = name
        self.uom            = uom
        self.description     = description

    def __repr__(self):
        return "<Exercise: %r, %r>" % (self.id, self.name)

