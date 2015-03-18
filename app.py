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
from db.Goods import Goods
from db.Comments import Comments

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

goods = Goods()
goods.create()

comments = Comments()
comments.create()
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

app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'
@app.route("/room/show/<room_id>", methods=["GET"])
def show_room(room_id):
  entries = Entry()
  items = entries.findAll(u"room_id='%s' ORDER BY room_id DESC" % room_id)

  goods = Goods()
  good = list()

  cookie = request.cookies.get("user_id")
  if cookie is None:
    uid = uuid.uuid4()
    session["user_id"] = uid
  else:
    good = goods.findAll("user_id='%s'" % cookie)
    session["user_id"] = cookie

  response = make_response(render_template("kpt-room.html", room_id=room_id, items=items, goods=good))
  response.set_cookie("user_id", session["user_id"])

  return response

@app.route("/new/comment/<kpt_id>", methods=["GET"])
def new_comment(kpt_id):
  entries = Entry()
  kpt = entries.findOne("id='%s'" % kpt_id)
  return render_template("comment.html", kpt=kpt)

@app.route("/post/comment/<kpt_id>", methods=["POST"])
def post_comment(kpt_id):
  req = {
    "kpt_id"    : request.form["kpt-id"].encode("utf-8")
    , "room_id" : request.form["room-id"].encode("utf-8")
    , "text"    : request.form["comment"].encode("utf-8")
  }

  entries = Entry()
  kpt = entries.findOne("id='%s'" % req["kpt_id"])

  if (kpt is None or kpt["room_id"] != req["room_id"]):
    return render_template("comment.html", kpt=kpt, error=u"投稿に失敗しました")

  comments = Comments()
  comment = {
    "kpt_id" : req["kpt_id"].decode("utf-8")
    , "text" : req["text"].decode("utf-8")
  }

  if comments.save(comment) is not None:
    return render_template("comment.html", kpt=kpt, error=u"投稿の保存に失敗しました")

  return render_template("comment.html", kpt=kpt, success="ok")

@app.route("/show/comment/<kpt_id>", methods=["GET"])
def show_comment(kpt_id):
  entries = Entry()
  kpt = entries.findOne("id='%s'" % kpt_id)
  return render_template("show-comment.html", kpt=kpt)

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
  goods = Goods()
  entries = Entry()

  if not sock: return
  good_sockets.append(sock)

  while True:
    obj = sock.receive();
    if obj is None: break

    req = json.loads(obj)
    uid = session["user_id"]
    kpt_id = req["kpt_id"]
    good_cnt = req["count"]

    if req["type"] == "add":
      good = {
        "user_id" : uid
        , "kpt_id" : kpt_id
      }
      if goods.save(good) is None:
        entries.update("good", good_cnt + 1, "id='%s'" % kpt_id)
    else:
      goods.delete("user_id='%s' and kpt_id='%s'" % (uid, kpt_id))
      entries.update("good", good_cnt - 1, "id='%s'" % kpt_id)

    for s in good_sockets:
      if parse_cookie(s.environ["HTTP_COOKIE"])["user_id"] == request.cookies.get("user_id"):
        obj = obj.replace("}", ',"user": 1}')
        print obj
      s.send(obj)

  good_sockets.remove(sock)
  sock.close()

def parse_cookie(pure_cookie):
  dic = dict()
  tmp_cookie = pure_cookie.split(';')

  for c in tmp_cookie:
    c = c.strip()
    parse = c.split('=')
    dic[parse[0]] = parse[1]

  return dic

if __name__ == "__main__":
  print "* Running on http://%s:%d" % (domain, port)
  print "* Restarting with reloader"
  app.jinja_env.add_extension('jinja2.ext.loopcontrols')

  server = WSGIServer((domain, port), app, handler_class=WebSocketHandler)
  server.serve_forever();
