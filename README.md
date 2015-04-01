# KPT-Tool
KPTを整理するためのツールを作ってみた

## USAGE
Web Socketを扱うためのライブラリの導入

gevent-websocket

    pip install gevent-websocket

Flask-Sockets

    pip install Flask-Sockets

config.jsonをconfigディレクトリ内に作成します。  

    {
      "db_path": "database.db"
      , "db_secret": "123456789"
      , "app_secret": "A0Zr98j/3yX R~XHH!jmN]LWX/,?RT"
      , "app_domain": "127.0.0.1"
      , "app_port": 5000
      , "salt": "$2a$12$KDhb/Zbwl7l7OxCg5N3HaO"
    }

## 起動

    python app.py
