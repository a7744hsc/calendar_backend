drop table if exists envents;
create TABLE events (id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT ,
  event_date DATETIME NOT NULL,created_date TIMESTAMP NOT NULL ,last_modified_date TIMESTAMP NOT NULL ,title CHAR(50) NOT NULL ,details TEXT(1000))
