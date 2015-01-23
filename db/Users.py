#!usr/bin/env python
# -*- coding: utf-8 -*-

from db.Base import Base

class Users(Base):
  table_name = "Users"
  model = """
    id INTEGER PRIMARY KEY AUTOINCREMENT
    , username TEXT NOT NULL
    , password TEXT NOT NULL
    , salt TEXT
    , admin INTEGER NOT NULL
  """
  scheme = None

  def __init__(self, scheme={}):
    super(Users, self).__init__()

    self.scheme = scheme

  def create(self):
    sql = u"DROP TABLE IF EXISTS %s;" % self.table_name
    self.cursor.execute(sql)

    sql = u"CREATE TABLE %s (%s);" % (self.table_name, self.model)
    self.cursor.execute(sql)

  def find(self, conditional=""):
    sql = ""

    if conditional:
      sql = u"SELECT * FROM %s WHERE %s;" % (self.table_name, conditional)
    else:
      sql = u"SELECT * FROM %s;" % (self.table_name)

    return self.cursor.execute(sql).fetchone()

  def save(self, items={}):
    keys = []
    values = []

    for k, v in items.iteritems():
      keys.append("'" + k + "'")
      values.append("'" + v + "'") if isinstance(v, str) else values.append(v)

    keys = ",".join(keys)
    values = ",".join(values)

    sql = u"INSERT INTO %s (%s) VALUES (%s);" % (self.table_name, keys, values)
    self.cursor.execute(sql)
    self.connection.commit()

  def delete(self, conditional=""):
    if not conditional:
      return

    sql = u"DELETE FROM %s WHERE %s;" % (self.table_name, conditional)
    self.cursor.execute(sql)
    self.connection.commit()
