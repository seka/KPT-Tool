#!usr/bin/env python
# -*- coding: utf-8 -*-

from flask import *
import json
import uuid

# websock ------
from gevent.pywsgi import WSGIServer
from geventwebsocket.handler import WebSocketHandler
from flask_sockets import Sockets

sockets = dict()
good_sockets = list()

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
  , "type"  : "keep"
  , "good"  : 4
}
test_entry2 = {
  "room_id" : "seka"
  , "entry" : u"この内容はテストです"
  , "type"  : "try"
  , "good"  : 5
}

entries = Entry()
entries.create()
entries.save(test_entry)
entries.save(test_entry)
entries.save(test_entry)
entries.save(test_entry2)
entries.save(test_entry2)
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
  return redirect("/room/show/" + req["room_id"])

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
  return redirect("/room/show/" + req["room_id"])

app.secret_key = "secret_test"
@app.route("/room/show/<room_id>", methods=["GET"])
def show_room(room_id):
  entries = Entry()
  items = entries.findAll(u"room_id='%s' ORDER BY room_id DESC" % room_id)

  res = make_response(
      render_template("kpt-room.html", room_id=room_id, items=items))

  cookie = request.cookies.get("user_id")
  if cookie is None:
    uid = uuid.uuid4()
    res.set_cookie("user_id", str(uid))
    session["user_id"] = uid
  else:
    session["user_id"] = cookie

  return res

@app.route("/websock/connect/room/<room_id>")
def connect_websock(room_id):
  sock = request.environ['wsgi.websocket'];
  entries = Entry()

  if not sock: return

  if not sockets.has_key(room_id): sockets[room_id] = list()
  sockets[room_id].append(sock)

  while True:
    obj = sock.receive();
    if obj is None: break

    req = json.loads(obj)

    entry = {
      "room_id" : req["room_id"]
      , "entry" : req["entry"]
      , "type"  : req["type"]
      , "good"  : 0
    }
    entries.save(entry)

    for s in sockets[room_id]:
      s.send(obj)

  sockets[room_id].remove(sock)
  sock.close()

@app.route("/websock/connect/good")
def connect_websock_good():
  sock = request.environ['wsgi.websocket'];

  if not sock: return
  good_sockets.append(sock)

  while True:
    obj = sock.receive();
    if obj is None: break

    req = json.loads(obj)
    print req

    for s in good_sockets:
      s.send(obj)

  good_sockets.remove(sock)
  sock.close()

if __name__ == "__main__":
  print "* Running on http://%s:%d" % (domain, port)
  print "* Restarting with reloader"
  server = WSGIServer((domain, port), app, handler_class=WebSocketHandler)
  server.serve_forever();
