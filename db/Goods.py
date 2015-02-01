#!usr/bin/env python
# -*- coding: utf-8 -*-

from db.Base import Base

class Goods(Base):
  table_name = "Goods"
  model = """
    id INTEGER PRIMARY KEY AUTOINCREMENT
    , user_id TEXT NOT NULL
    , kpt_id INTEGER NOT NULL
  """
  scheme = None

  def __init__(self, scheme={}):
    super(Goods, self).__init__()

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

    if conditional:
      sql = u"UPDATE %s SET %s='%s' WHERE %s;" % (self.table_name, colum, value, conditional)
    else:
      sql = u"UPDATE %s SET %s='%s';" % (self.table_name, colum, value)

    self.cursor.execute(sql)
    self.connection.commit()
