import sqlite3

class Base(object):
  instance = None

  class __Base:
    def __init__(self, arg):
        self.path = "database.db"
        self.connection = sqlite3.connect(self.path)

  def _init_(self, args):
    if not self.instance:
      self.instance = Base.__Base(arg)

  def __getattr__(self):
    return getattr(self.instance)

  def checkConection():
    return self.connection

  def create(database):
    pass

  def find(database, key={}):
    pass

  def save(database, obj={}):
    pass

  def delete(database, key={}):
    pass


