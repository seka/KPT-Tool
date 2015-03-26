#!usr/bin/env python
# -*- coding: utf-8 -*-

# models --------------------------
from Base import Base
from Users import Users
from Rooms import Rooms
from Entry import Entry
from Goods import Goods
from Comments import Comments

test_user = {
  "username" : "test"
  , "password" : "29148931"
  , "salt" : "1234"
  , "admin" : "1"
}
users = Users()
users.create()
users.save(test_user)

test_room = {
  "room_id" : "seka"
  , "password" : "29148931"
}
test_room2 = {
  "room_id" : "test"
  , "password" : "29148931"
}

rooms = Rooms()
rooms.create()
rooms.save(test_room)
rooms.save(test_room2)

test_entry = {
  "room_id" : "seka"
  , "entry" : u"この内容はテストです"
  , "type"  : "keep"
  , "good"  : 4
}
test_entry2 = {
  "room_id" : "seka"
  , "entry" : u"この内容はテストです"
  , "type"  : "try"
  , "good"  : 5
}

entries = Entry()
entries.create()
entries.save(test_entry)
entries.save(test_entry)
entries.save(test_entry)
entries.save(test_entry2)
entries.save(test_entry2)

goods = Goods()
goods.create()

test_comment = {
  "kpt_id" : 1
  , "text" : u"テストのコメントです"
}

test_comment2 = {
  "kpt_id" : 1
  , "text" : u"テストのコメントです2"
}
test_comment3 = {
  "kpt_id" : 2
  , "text" : u"テスト2のコメントです"
}

comments = Comments()
comments.create()
comments.save(test_comment)
comments.save(test_comment2)
comments.save(test_comment3)
