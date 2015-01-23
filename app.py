#!usr/bin/env python
# -*- coding: utf-8 -*-

from flask import *
from db.Base import Base
from db.Users import Users

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
# end --------------------

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
    "username" : request.form["username"].rstrip()
    , "password" : request.form["password"].rstrip()
  }

  users = Users()
  user = users.find("username='{username}'".format(**req))

  if user is None or user["password"] != req["password"]:
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
