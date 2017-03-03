drop table if exists envents;
create TABLE events (id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT ,
  event_date DATETIME ,created_date TIMESTAMP,last_modified_date TIMESTAMP,title CHAR(50),details TEXT(1000))
