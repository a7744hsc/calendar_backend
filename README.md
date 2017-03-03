1.建立mysql数据库,
    create database calendar;
    create TABLE events (id INT NOT NULL PRIMARY KEY AUTOINCREMENT ,date DATETIME ,created_date TIMESTAMP,last_modified_date TIMESTAMP,title CHAR(50),details TEXT(1000))






api:
 calendar/v1.0/events : [GET]get all events
                        [POST] save a new event
                        post with header "Content-Type: application/json"
                        body:{"title":"first from post",
                                "details":"still no details",
                                "event_date":"2017-03-03 11:50:00"
                            }
 calendar/v1.0/events?date=yyyy-mm-dd : [GET]get all events for special day










Start flask:
export FLASK_DEBUG=1
export FLASK_APP=main.py
flask run




sql tips:
 select * from sqlite_master WHERE type = "table";
