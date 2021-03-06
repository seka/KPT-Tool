#!usr/bin/env python
# -*- coding: utf-8 -*-

import sqlite3
import json

class Base(object):
  instance = None

  def __new__(cls, *args, **kwargs):
    if not cls.instance:
      cls.instance = super(Base, cls).__new__(cls, *args, **kwargs)
    return cls.instance

  def __init__(self):
    # 起動した場所からのpath
    f = open("./config/config.json", "r")
    config = json.load(f)

    self.path = config["db_path"]
    self.secret = config["db_secret"]

    self.connection = sqlite3.connect(self.path)
    self.connection.row_factory = sqlite3.Row
    self.cursor = self.connection.cursor()

  def getConection():
    return self.connection

