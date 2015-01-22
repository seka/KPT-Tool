#!usr/bin/env python
# -*- coding: utf-8 -*-

import sqlite3

class Base(object):
  instance = None

  def __new__(cls, *args, **kwargs):
    if not cls.instance:
      cls.instance = super(Base, cls).__new__(cls, *args, **kwargs)
    return cls.instance

  def __init__(self):
    self.path = "db/database.db"
    self.connection = sqlite3.connect(self.path)
    self.cursor = self.connection.cursor()

  def getConection():
    return self.connection

