#!usr/bin/env python
# -*- coding: utf-8 -*-

from flask import *
from db.Base import Base
from db.Users import Users
from db.Rooms import Rooms

app = Flask(__name__)
app.debug = True
app.config["SEND_FILE_MAX_AGE_DEFAULT"] = 0

# test --------------------
test_user = {
  "username" : "test"
  , "password" : "29148931"
  , "salt" : "1234"
  , "admin" : "1"
}
users = Users()
users.create()
users.save(test_user)

rooms = Rooms()
rooms.create()
# end ---------------------

@app.before_request
def before_request():
  base = Base()
  g.db = base.connection

@app.after_request
def after_request(response):
  g.db.close()
  return response

@app.route("/")
def index():
  return render_template("top.html")

@app.route("/create-room", methods=["GET"])
def create_room():
  return render_template("create-room.html")

@app.route('/signin', methods=["POST"])
def signin():
  req = {
    "username" : request.form["username"]
    , "password" : request.form["password"].encode("utf-8")
  }

  user_model = Users()
  user = user_model.find("username='%s'" % req["username"])

  if user is None:
    return render_template("login.html", error=u"IDまたはパスワードが違います")

  hashpw = user["password"]
  salt = user["salt"].encode("utf-8")

  if user_model.check_passwd(req["password"], salt, hashpw) != True:
    return render_template("login.html", error=u"IDまたはパスワードが違います")

  return render_template("test.html")

@app.route('/signout', methods=["POST"])
def signout():
  pass

@app.route('/signup', methods=["POST"])
def signup():
  req = {
    "room_id" : request.form["room-id"].encode("utf-8")
    , "password" : request.form["password"].encode("utf-8")
  }

  room_model = Rooms()
  room = room_model.find("room_id='%s'" % req["room_id"])

  if room:
    return render_template("create-room.html", error=u"同名のルームが存在します")

  room_model.save(req)

  return redirect("/room/show/" + req["room_id"])

@app.route("/room/show/<room_id>", methods=["GET"])
def show_room(room_id):
  return render_template("test.html")

if __name__ == "__main__":
  app.run()
