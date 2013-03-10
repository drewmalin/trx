# API!
#
# Many of the JSON strings constructed below are done so in an odd manner (e.g. having a single line do something
# like 'json+="{"') -- this is purely for readability.
#
# Current API:
# 
# All Users:
#     /users/
# User with id = user_id:                        
#     /users/<user_id>
# All workouts for user with id = user_id:                    
#     /users/<user_id>/workouts/
# Workout with id workout_id for user with id = user_id:
#     /users/<user_id>/workouts/<workout_id>
# All workotus with exercise = exercise_name for user with id = user_id:
#     /users/<user_id>/exercises/<exercise_name/

from utilities import db
import flask, flask.views
from models import *
from trx import app
from datetime import datetime, date
from decorators import *
from flask.ext.login import *
from sqlalchemy import Date, cast

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

@app.route('/exercisedropdown/')
@crossdomain(origin='*')
def request_all_exercises():
    exerciseFilter = request.args.get("term")
    filterList = exerciseFilter.split(", ")

    jsonStr = "["
    exercises = Exercise.query.order_by(Exercise.name.asc())

    for exercise in exercises:
        if any(exercise.name in s for s in filterList):
            continue
        else:
            jsonStr += "\"" + exercise.name + "\","
    jsonStr = jsonStr[:-1] + "]"

    return jsonStr

@app.route('/userdropdown/')
@crossdomain(origin='*')
def request_all_users():
    userFilter = request.args.get("term")
    filterList = userFilter.split(", ")

    jsonStr = "["
    users = User.query.order_by(User.username.asc())

    for user in users:
        if any(user.username in s for s in filterList):
            continue
        elif user.id == current_user.id:
            continue
        else:
            jsonStr += "{\"value\":\"" + str(user.id) + "\","
            jsonStr += "\"label\":\"" + user.username + "\"},"
    jsonStr = jsonStr[:-1] + "]"

    return jsonStr

@app.route('/workouts/')
@crossdomain(origin='*')
def request_all_workouts():

    # Get Exercise using exercise name from query
    exercise = Exercise.query.filter_by(name=request.args.get("exercises")).first()
    # Get ID Numbers of all requested users (plus current)
    userIDList = compileUserIDList(request.args.get("users"))
    # Get unique list of dates for all shared workouts for exercise
    uniqueDateList = compileUniqueDates(userIDList, exercise)
    # Get results for each user in the id list for each workout corresponding to each unique date for exercise
    workoutDataList = compileWorkoutData(userIDList, exercise, uniqueDateList)

    return flask.jsonify(exercise=exercise.name,units=exercise.uom,dates=dateListAsStrings(uniqueDateList),data=workoutDataList)


#### Here be utility functions ####


# Parm: strList -- list of comma+space-separated usernames.
# Function splits each name into a list, then retrieves each user id from the database, returning an
# array of ids
def compileUserIDList(strList):
    idList = []
    userList = ""
    if strList is None:
        pass
    else:
        userList = strList.split(",")
        for userID in userList:
            if userID == "":
                continue
            else:
                idList.append(User.query.filter_by(id=userID).first().id)
    idList.append(current_user.id)
    return idList

# Parm: idList -- array of ids
# Parm: exercise -- Exercise database object
# Function gets list of date objects from database. For all workouts in the database that were
# completed by users with id numbers in idList, and for exercises equal to exercise, all date objects
# for each workout are retrieved in chronological order and returned as an array
def compileUniqueDates(idList, exercise):
    dateList = []
    allSharedWorkouts = Workout.query.filter(Workout.user_id.in_(idList)).order_by(Workout.date.asc())

    for workout in allSharedWorkouts:
        if workout.date in dateList or workout.exercise_id != exercise.id:
            continue
        else:
            dateList.append(workout.date)
    return dateList

# Parm: dateList -- array of date objects
# Function returns date objects as formatted strings
def dateListAsStrings(dateList):
    dateStrList = []
    for date in dateList:
        dateStrList.append(date.strftime('%m/%d/%Y'))
    return dateStrList

# Parm: idList -- array of ids
# Parm: exercise -- Exercise database object
# Parm: dateList -- array of date objects
# Function constructs data on each workout for each user in the idList. For each date in the date list,
# grab the workout for each user (id) and the exercise, record the results in an array [index, result],
# then return as a larger array: [name, [index, result], [index, result]]
def compileWorkoutData(idList, exercise, dateList):
    workoutSuperList = []

    for userId in idList:
        i = 0
        userDict = {}
        dataList = []
        for date in dateList:
            data = []
            contextWorkout = Workout.query.filter_by(user_id=int(userId), exercise_id=exercise.id, date=date).first()
            if not contextWorkout:
                pass
            else:
                data.append(i)
                data.append(contextWorkout.units)
                dataList.append(data)
            i=i+1
        userDict["name"] = User.query.filter_by(id=userId).first().username
        userDict["data"] = dataList

        workoutSuperList.append(userDict)

    return workoutSuperList