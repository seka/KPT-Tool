drop table if exists Users;
create table Users (
  id integer primary key autoincrement
  , username string not null
  , password string not null
  , admin bool not null
);
