import sqlite3

class Base(object):
  instance = None

  class __Base:
    def __init__(self, argv):
      self.path = "database.db"
      self.connection = sqlite3.connect(self.path)

  def __new__(self, *argc, **argv):
    if not self.instance:
      self.instance = Base.__Base(argv)
    return self.instance

  def getConection():
    return self.connection

  def create(database):
    pass

  def find(database, key={}):
    pass

  def save(database, obj={}):
    pass

  def delete(database, key={}):
    pass


