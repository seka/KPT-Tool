#!usr/bin/env python
# -*- coding: utf-8 -*-

def parse_cookie(pure_cookie):
  dic = dict()
  tmp_cookie = pure_cookie.split(';')

  for c in tmp_cookie:
    c = c.strip()
    parse = c.split('=')
    dic[parse[0]] = parse[1]

  return dic
