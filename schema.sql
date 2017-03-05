drop table if exists envents;
create TABLE events (id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT ,  event_start DATETIME NOT NULL,
  event_end DATETIME NOT NULL,created_date TIMESTAMP NOT NULL ,last_modified_date TIMESTAMP NOT NULL ,event_owner CHAR(50) NOT NULL ,title CHAR(50) NOT NULL ,details TEXT(1000));
