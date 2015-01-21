#!usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask, render_template

app = Flask(__name__)
app.debug = True
app.config["SEND_FILE_MAX_AGE_DEFAULT"] = 0

@app.route("/")
def index():
    return render_template("login.html")

@app.route('/signin', methods=["POST"])
def signin():
    pass

@app.route('/signout', methods=["POST"])
def signout():
    pass

@app.route('/signup', methods=["POST"])
def signout():
    pass

if __name__ == "__main__":
    app.run()