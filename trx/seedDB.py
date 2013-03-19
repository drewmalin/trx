from flask.ext.sqlalchemy import SQLAlchemy
from utilities import db
from models import Exercise

def seed(reset):

    if (reset == True):
        # Drop/recreate database
        db.drop_all()
        db.create_all()

        # Create default data
        db.session.add(Exercise("Deadlift", "Pounds", ""))
        db.session.add(Exercise("Squat (Clean)", "Pounds", ""))
        db.session.add(Exercise("Squat (Back)", "Pounds", ""))
        db.session.add(Exercise("Squat (Overhead)", "Pounds", ""))
        db.session.add(Exercise("Squat (Front)", "Pounds", ""))
        db.session.add(Exercise("Press (Push)", "Pounds", ""))
        db.session.add(Exercise("Press (Strict)", "Pounds", ""))
        db.session.add(Exercise("Pullup", "Repetition", ""))
        db.session.add(Exercise("Snatch", "Pounds", ""))

        db.session.commit()

        