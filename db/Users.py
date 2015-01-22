#!usr/bin/env python
# -*- coding: utf-8 -*-

from db.Base import Base

class Users(Base):
  table_name = "Users"
  model = """
    id INTEGER PRIMARY KEY AUTOINCREMENT
    , username STRING NOT NULL
    , password STRING NOT NULL
    , salt STRING NOY NULL
    , admin INTEGER NOT NULL
  """
  scheme = None

  def __init__(self, scheme={}):
    super(Users, self).__init__()

    self.scheme = scheme

  def create(self):
    sql = "DROP TABLE IF EXISTS %s;" % self.table_name
    self.cursor.execute(sql)

    sql = "CREATE TABLE %s (%s);" % (self.table_name, self.model)
    self.cursor.execute(sql)

  def find(conditional=""):
    if conditional:
      sql += "SELECT * FROM %s WHERE %s;" % (self.table_name, conditional)
    else:
      sql = "SELECT * FROM %s;" % (table_name)
    self.cursor.execute(sql)

  def save(self, items={}):
    keys = []
    values = []

    for k, v in items.iteritems():
      keys.append("'" + k + "'")
      values.append("'" + v + "'")

    keys = ",".join(keys)
    values = ",".join(values)

    sql = "INSERT INTO %s (%s) VALUES (%s);" % (self.table_name, keys, values)
    self.cursor.execute(sql)
    self.connection.commit()


  def delete(conditional=""):
    if not conditional:
      return

    sql = "DELETE FROM %s WHERE %s;" % (self.table_name, conditional)
    self.cursor.execute(sql)
    self.connection.commit()
