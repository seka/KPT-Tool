#!usr/bin/env python
# -*- coding: utf-8 -*-

from Base import Base
import bcrypt

class Rooms(Base):
  table_name = "Rooms"
  model = """
    id INTEGER PRIMARY KEY AUTOINCREMENT
    , room_id TEXT NOT NULL
    , password TEXT DEFAULT ''
  """
  scheme = None

  def __init__(self, scheme={}):
    super(Rooms, self).__init__()

    self.scheme = scheme

  def hash_passwd(self, passwd="", salt=""):
    return bcrypt.hashpw(passwd, salt)

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

  def save(self, items={}, salt="$2a$12$KDhb/Zbwl7l7OxCg5N3HaO"):
    keys = []
    values = []

    for k, v in items.iteritems():
      if k == "password": v = self.hash_passwd(v, salt)
      keys.append("'" + k + "'")
      values.append("'" + v + "'")

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

