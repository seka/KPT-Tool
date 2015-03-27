#!usr/bin/env python
# -*- coding: utf-8 -*-

from flask import *
import json
import uuid

# websock ------
from gevent.pywsgi import WSGIServer
from geventwebsocket.handler import WebSocketHandler
from flask_sockets import Sockets

kpt_sockets = dict()
good_sockets = list()
comment_sockets = dict()

# models -------
from db.Base import Base
from db.Users import Users
from db.Rooms import Rooms
from db.Entry import Entry
from db.Goods import Goods
from db.Comments import Comments

# utile --------
from services.utils.cookie import *

# app configs -------
app = Flask(__name__)

f = open("./config/config.json", "r")
config = json.load(f)
domain = config["app_domain"]
port   = config["app_port"]

app.debug = True
app.secret_key = config["app_secret"]

app.config["SEND_FILE_MAX_AGE_DEFAULT"] = 0

@app.route("/")
def render_top():
  return render_template("top.html")

@app.route("/create-room", methods=["GET"])
def render_make_room():
  return render_template("create-room.html")

@app.route("/signin-room", methods=["GET"])
def render_signin():
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

@app.route("/room/show/<room_id>", methods=["GET"])
def render_room(room_id):
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
  # response.set_cookie("user_id", session["user_id"])
  response.set_cookie("user_id", "test")

  return response

@app.route("/new/comment/<kpt_id>", methods=["GET"])
def render_comment(kpt_id):
  entries = Entry()
  kpt = entries.findOne("id='%s'" % kpt_id)
  return render_template("comment.html", kpt=kpt)

@app.route("/post/comment/<kpt_id>", methods=["POST"])
def new_comment(kpt_id):
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

  # websocketによる配信
  comment.update({"type": "append"})
  obj = json.dumps(comment)

  if comment_sockets.has_key(kpt_id):
    for s in comment_sockets[kpt_id]:
      s.send(obj)

  return render_template("comment.html", kpt=kpt, success="ok")

@app.route("/show/comment/<kpt_id>", methods=["GET"])
def show_comment(kpt_id):
  comments = Comments()
  comment = comments.findAll("kpt_id='%s'" % kpt_id)
  return render_template("show-comment.html", items=comment, kpt_id=kpt_id)

@app.route("/websock/connect/room/<room_id>")
def connect_kpt_websock(room_id):
  sock = request.environ['wsgi.websocket'];
  entries = Entry()

  if not sock: return

  if not kpt_sockets.has_key(room_id): kpt_sockets[room_id] = list()
  kpt_sockets[room_id].append(sock)

  while True:
    obj = sock.receive();
    if obj is None: break

    req = json.loads(obj)

    if req["type"] in {"keep", "problem", "try"}:
      entry = {
        "room_id" : req["room_id"]
        , "entry" : req["entry"]
        , "type"  : req["type"]
        , "good"  : 0
      }
      entries.save(entry)

    if req["type"] in "remove":
      entries.delete("id=%s" % req["kpt_id"])

    for s in kpt_sockets[room_id]:
      s.send(obj)

  kpt_sockets[room_id].remove(sock)
  sock.close()

@app.route("/websock/connect/good")
def connect_good_websock():
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
      s.send(obj)

  good_sockets.remove(sock)
  sock.close()

@app.route("/websock/connect/comment/<kpt_id>")
def connect_comment_websock(kpt_id):
  sock = request.environ['wsgi.websocket'];
  comments = Comments()

  if not sock: return

  if not comment_sockets.has_key(kpt_id): comment_sockets[kpt_id] = list()
  comment_sockets[kpt_id].append(sock)

  while True:
    obj = sock.receive();
    if obj is None: break

    req = json.loads(obj)

    if req["type"] in "remove":
      print "test:", req["commentId"]
      comments.delete("id=%s" % req["commentId"])
      for s in comment_sockets[kpt_id]:
        s.send(obj)

  comment_sockets[kpt_id].remove(sock)
  sock.close()

if __name__ == "__main__":
  print "* Running on http://%s:%d" % (domain, port)
  print "* Restarting with reloader"

  app.jinja_env.add_extension('jinja2.ext.loopcontrols')

  server = WSGIServer((domain, port), app, handler_class=WebSocketHandler)
  server.serve_forever();
