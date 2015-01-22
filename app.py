#!usr/bin/env python
# -*- coding: utf-8 -*-

from flask import *
from db.Base import Base
from db.Users import Users

app = Flask(__name__)
app.debug = True
app.config["SEND_FILE_MAX_AGE_DEFAULT"] = 0

test_user = {
    "username" : "test"
    , "password" : "29148931"
    , "salt" : "1234"
    , "admin" : "1"
}

print "test ----------"
users = Users()
users2 = Users()
print users, users2

print "test1 ----------"
users = Users()
users2 = Users()
print users, users2

print "test2 ----------"
users = Users()
users2 = Users()
print users, users2

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
    return render_template("login.html")

@app.route('/signin', methods=["POST"])
def signin():
  req = {
    "username" : request.form["username"]
    , "password" : request.form["password"]
  }

  user = test_user
  result = user.has_key(req["username"])

  if result == False or req["password"] != req["password"]:
    return render_template("login.html", error="IDまたはパスワードが違います")
  return render_template("test.html")


@app.route('/signout', methods=["POST"])
def signout():
    pass

@app.route('/signup', methods=["POST"])
def signup():
    pass

if __name__ == "__main__":
    app.run()
