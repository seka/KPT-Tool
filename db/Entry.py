#!usr/bin/env python
# -*- coding: utf-8 -*-

from Base import Base

class Entry(Base):
  table_name = "Entry"
  model = """
    id INTEGER PRIMARY KEY AUTOINCREMENT
    , room_id TEXT NOT NULL
    , entry TEXT NOT NULL
    , type TEXT NOT NULL
    , good INTEGER DEFAULT 0
  """
  scheme = None

  def __init__(self, scheme={}):
    super(Entry, self).__init__()

    self.scheme = scheme

  def create(self):
    sql = u"DROP TABLE IF EXISTS %s;" % self.table_name
    self.cursor.execute(sql)

    sql = u"CREATE TABLE %s (%s);" % (self.table_name, self.model)
    self.cursor.execute(sql)

  def _find(self, conditional=""):
    sql = ""

    if conditional:
      sql = u"SELECT * FROM %s WHERE %s;" % (self.table_name, conditional)
    else:
      sql = u"SELECT * FROM %s;" % (self.table_name)

    return self.cursor.execute(sql)

  def findOne(self, conditional=""):
    return self._find(conditional).fetchone()

  def findAll(self, conditional=""):
    return self._find(conditional).fetchall()

  def save(self, items={}):
    keys = []
    values = []

    for k, v in items.iteritems():
      keys.append("'" + k + "'")
      values.append("'" + unicode(v) + "'")

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

  def update(self, colum, value, conditional):
    sql = ""

    if not colum or not value:
      return

    if conditional:
      sql = u"UPDATE %s SET %s='%s' WHERE %s;" % (self.table_name, colum, value, conditional)
    else:
      sql = u"UPDATE %s SET %s='%s';" % (self.table_name, colum, value)

    self.cursor.execute(sql)
    self.connection.commit()
