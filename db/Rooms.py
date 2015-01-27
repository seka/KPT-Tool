#!usr/bin/env python
# -*- coding: utf-8 -*-

from db.Base import Base
import bcrypt

class Rooms(Base):
  table_name = "Rooms"
  model = """
    id INTEGER PRIMARY KEY AUTOINCREMENT
    , room_id TEXT NOT NULL
    , password TEXT DEFAULT ''
    , salt TEXT NOT NULL
  """
  scheme = None

  def __init__(self, scheme={}):
    super(Rooms, self).__init__()

    self.scheme = scheme

  def _generate_passwd(self, passwd=""):
    salt = bcrypt.gensalt()
    hashpw = bcrypt.hashpw(passwd, salt)
    return ["'%s'" % hashpw, "'%s'" % salt]

  def check_passwd(self, passwd, hashed, hashpw):
    if bcrypt.hashpw(passwd, hashed) != hashpw:
      return False
    return True

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

    if items.has_key("salt"):
      del items["salt"]

    for k, v in items.iteritems():
      if k == "password":
        keys.extend(["'password'", "'salt'"])
        values.extend(self._generate_passwd(v))
        continue

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

