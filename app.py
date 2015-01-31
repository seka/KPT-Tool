#!usr/bin/env python
# -*- coding: utf-8 -*-

from flask import *
import json

# websock ------
from gevent.pywsgi import WSGIServer
from geventwebsocket.handler import WebSocketHandler
sockets = set()

# models -------
from db.Base import Base
from db.Users import Users
from db.Rooms import Rooms
from db.Entry import Entry

# app configs -------
domain = "127.0.0.1"
port = 5000

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

test_room = {
  "room_id" : "seka"
  , "password" : "29148931"
}
test_room2 = {
  "room_id" : "test"
  , "password" : "29148931"
}

rooms = Rooms()
rooms.create()
rooms.save(test_room)
rooms.save(test_room2)

test_entry = {
  "room_id" : "seka"
  , "entry" : u"この内容はテストです"
  , "good"  : 4
}
entries = Entry()
entries.create()
entries.save(test_entry)
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

@app.route("/signin-room", methods=["GET"])
def signin_room():
  return render_template("signin-room.html")

@app.route('/signin', methods=["POST"])
def signin():
  req = {
    "room_id" : request.form["room-id"]
    , "password" : request.form["password"].encode("utf-8")
  }

  room_model = Rooms()
  room = room_model.find("room_id='%s'" % req["room_id"])

  if room is None:
    return render_template("signin-room.html", error=u"IDまたはパスワードが違います")

  hashpw = room["password"]
  salt = room["salt"].encode("utf-8")

  if room_model.check_passwd(req["password"], salt, hashpw) != True:
    return render_template("signin-room.html", error=u"IDまたはパスワードが違います")

  return render_template("kpt-room.html", room_id=req["room_id"])

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

  if room: return render_template("create-room.html", error=u"同名のルームが存在します")

  room_model.save(req)
  return redirect("/room/show" + req["room_id"])

@app.route("/room/show/<room_id>", methods=["GET"])
def show_room(room_id):
  print "room_id"
  return render_template("test.html", room_id=room_id)

@app.route("/websock/connect")
def connect_websock():
  sock = request.environ['wsgi.websocket'];

  if not sock: return
  sockets.add(sock)

  while True:
    obj = sock.receive();
    if obj is None: break

    req = json.loads(obj)
    print req

    for s in sockets:
      s.send(obj)

  sockets.remove(sock)
  sock.close()

if __name__ == "__main__":
  print "* Running on http://%s:%d" % (domain, port)
  print "* Restarting with reloader"
  server = WSGIServer((domain, port), app, handler_class=WebSocketHandler)
  server.serve_forever();
