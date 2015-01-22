# -*- coding: utf-8 -*-

import Base

class Users(Base):
  model = None
  scheme = None
  db_name = "Users"

  def __init__(self, arg={}):
    self.scheme = {
      "id" : arg.user_id
      , "username" : arg.username
      , "password" : arg.password
      , "salt"     : arg.salt
      , "user_level" : arg.user_level
    }


