#!usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask, render_template, request

app = Flask(__name__)
app.debug = True
app.config["SEND_FILE_MAX_AGE_DEFAULT"] = 0

test_user = {
  "test" : {
    "name" : "test"
    , "password" : "29148931"
  }
}

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

  if result == False or user[req["username"]]["password"] != req["password"]:
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
